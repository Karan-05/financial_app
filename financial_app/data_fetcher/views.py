# data_fetcher/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from .models import StockData
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .utils import create_stock_price_plot
import pandas as pd
import numpy as np
import io
from django.http import JsonResponse
from .models import StockData
import pandas as pd
import numpy as np
import joblib
from django.http import JsonResponse
from .models import StockData, StockPrediction
from datetime import timedelta
from django.http import FileResponse
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO


def backtest_strategy(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        # Get parameters from form data
        try:
            initial_investment = float(request.POST.get('initial_investment', 10000))
            short_window = int(request.POST.get('short_window', 50))
            long_window = int(request.POST.get('long_window', 200))
            symbol = request.POST.get('symbol', 'AAPL').upper()
            output_format = request.POST.get('output_format', 'pdf')
        except ValueError as e:
            error_message = f'Invalid input parameters: {e}'
            return render(request, 'data_fetcher/backtest_form.html', {'error_message': error_message})
        
        # Validate that short_window is less than long_window
        if short_window >= long_window:
            error_message = 'Short window must be less than long window.'
            return render(request, 'data_fetcher/backtest_form.html', {
                'error_message': error_message,
                'initial_investment': initial_investment,
                'short_window': short_window,
                'long_window': long_window,
                'symbol': symbol,
            })
        
        # Fetch historical data from the database
        qs = StockData.objects.filter(symbol=symbol).order_by('date')
        if not qs.exists():
            error_message = f"No historical data available for {symbol}."
            return render(request, 'data_fetcher/backtest_form.html', {
                'error_message': error_message,
                'initial_investment': initial_investment,
                'short_window': short_window,
                'long_window': long_window,
                'symbol': symbol,
            })
        
        # Convert queryset to DataFrame
        data = pd.DataFrame.from_records(qs.values())
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)
        data.sort_index(inplace=True)
        
        # Backtesting Logic

        # Calculate moving averages
        data['short_mavg'] = data['close_price'].rolling(window=short_window, min_periods=1).mean()
        data['long_mavg'] = data['close_price'].rolling(window=long_window, min_periods=1).mean()

        # Create signals
        data['signal'] = 0.0
        data['signal'][short_window:] = np.where(
            data['short_mavg'][short_window:] > data['long_mavg'][short_window:], 1.0, 0.0)
        data['positions'] = data['signal'].diff()

        # Initialize portfolio
        portfolio = pd.DataFrame(index=data.index)
        portfolio['positions'] = data['signal']
        portfolio['close_price'] = data['close_price']
        portfolio['holdings'] = portfolio['positions'] * portfolio['close_price']
        portfolio['cash'] = initial_investment - (portfolio['positions'].diff() * portfolio['close_price']).fillna(0).cumsum()
        portfolio['total'] = portfolio['holdings'] + portfolio['cash']
        portfolio['returns'] = portfolio['total'].pct_change().fillna(0)

        # Calculate performance metrics
        total_return = portfolio['total'].iloc[-1] - initial_investment
        total_return_percent = (portfolio['total'].iloc[-1] / initial_investment - 1) * 100

        # Max drawdown
        roll_max = portfolio['total'].cummax()
        daily_drawdown = portfolio['total'] / roll_max - 1.0
        max_drawdown = daily_drawdown.min()

        # Number of trades executed
        number_of_trades = int(data['positions'].abs().sum())

        # Prepare results
        result = {
            'initial_investment': round(initial_investment, 2),
            'final_investment_value': round(portfolio['total'].iloc[-1], 2),
            'total_return': round(total_return, 2),
            'total_return_percent': round(total_return_percent, 2),
            'max_drawdown_percent': round(max_drawdown * 100, 2),
            'number_of_trades': number_of_trades,
        }

        if action == 'backtest':
            # Render the results on the same page
            return render(request, 'data_fetcher/backtest_form.html', {
                'result': result,
                'initial_investment': initial_investment,
                'short_window': short_window,
                'long_window': long_window,
                'symbol': symbol,
                'output_format': output_format,
            })
        elif action == 'generate_report':
            # Store parameters in session and redirect to generate_report view
            request.session['backtest_params'] = {
                'initial_investment': initial_investment,
                'short_window': short_window,
                'long_window': long_window,
                'symbol': symbol,
                'output_format': output_format,
            }
            return redirect('generate_report')
    else:
        # GET request: render the form
        return render(request, 'data_fetcher/backtest_form.html')

def generate_report(request):
    # Retrieve parameters from session
    backtest_params = request.session.get('backtest_params')
    if not backtest_params:
        return HttpResponse('No backtest parameters found. Please run a backtest first.', status=400)
    
    initial_investment = backtest_params['initial_investment']
    short_window = backtest_params['short_window']
    long_window = backtest_params['long_window']
    symbol = backtest_params['symbol']
    output_format = backtest_params['output_format']

    # Fetch historical data from the database
    qs = StockData.objects.filter(symbol=symbol).order_by('date')
    if not qs.exists():
        return HttpResponse(f"No historical data available for {symbol}.", status=400)
    
    # Convert queryset to DataFrame
    data = pd.DataFrame.from_records(qs.values())
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    data.sort_index(inplace=True)
    
    # Backtesting Logic

    # Calculate moving averages
    data['short_mavg'] = data['close_price'].rolling(window=short_window, min_periods=1).mean()
    data['long_mavg'] = data['close_price'].rolling(window=long_window, min_periods=1).mean()

    # Create signals
    data['signal'] = 0.0
    data['signal'][short_window:] = np.where(
        data['short_mavg'][short_window:] > data['long_mavg'][short_window:], 1.0, 0.0)
    data['positions'] = data['signal'].diff()

    # Initialize portfolio
    portfolio = pd.DataFrame(index=data.index)
    portfolio['positions'] = data['signal']
    portfolio['close_price'] = data['close_price']
    portfolio['holdings'] = portfolio['positions'] * portfolio['close_price']
    portfolio['cash'] = initial_investment - (portfolio['positions'].diff() * portfolio['close_price']).fillna(0).cumsum()
    portfolio['total'] = portfolio['holdings'] + portfolio['cash']
    portfolio['returns'] = portfolio['total'].pct_change().fillna(0)

    # Calculate performance metrics
    total_return = portfolio['total'].iloc[-1] - initial_investment
    total_return_percent = (portfolio['total'].iloc[-1] / initial_investment - 1) * 100

    # Max drawdown
    roll_max = portfolio['total'].cummax()
    daily_drawdown = portfolio['total'] / roll_max - 1.0
    max_drawdown = daily_drawdown.min()

    # Number of trades executed
    number_of_trades = int(data['positions'].abs().sum())

    # For illustration, let's create dummy predicted prices (or use actual predictions)
    data['predicted_price'] = data['close_price'].shift(-1).fillna(method='ffill')

    # Generate the chart
    chart = create_stock_price_plot(
        dates=data.index.strftime('%Y-%m-%d'),
        actual_prices=data['close_price'],
        predicted_prices=data['predicted_price']
    )

    # Prepare results
    result = {
        'initial_investment': round(initial_investment, 2),
        'final_investment_value': round(portfolio['total'].iloc[-1], 2),
        'total_return': round(total_return, 2),
        'total_return_percent': round(total_return_percent, 2),
        'max_drawdown_percent': round(max_drawdown * 100, 2),
        'number_of_trades': number_of_trades,
    }

    if output_format == 'pdf':
        # Render the HTML template with context
        html = render_to_string('data_fetcher/report_template.html', {
            'result': result,
            'chart': chart,
        })
        
        # Create a PDF file
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="performance_report_{symbol}.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error generating PDF report', status=500)
        return response
    
    elif output_format == 'json':
        # Return the data as JSON
        return JsonResponse({
            'result': result,
            # Optionally include the base64-encoded chart
            'chart': chart,
        })
    else:
        return HttpResponse('Invalid output format specified.', status=400)
def home(request):
    return render(request, 'data_fetcher/home.html')

from django.shortcuts import render

def predict_stock_prices(request):
    SYMBOL = 'AAPL'
    MODEL_PATH = 'models/stock_prediction_model.pkl'

    # Load the model
    try:
        model = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        return JsonResponse({'error': 'Model file not found.'}, status=500)

    # Fetch historical data
    qs = StockData.objects.filter(symbol=SYMBOL).order_by('date')
    if not qs.exists():
        return JsonResponse({'error': 'No historical data available.'}, status=400)

    data = pd.DataFrame.from_records(qs.values())
    features = data[['open_price', 'high_price', 'low_price', 'close_price', 'volume']]

    # Generate predictions for the next 30 days
    last_known_date = data['date'].iloc[-1]
    predictions = []
    for i in range(1, 31):
        # For simplicity, use the last known feature set
        X = features.iloc[-1].values.reshape(1, -1)
        predicted_price = model.predict(X)[0]
        prediction_date = last_known_date + timedelta(days=i)
        predictions.append({
            'date': prediction_date.strftime('%Y-%m-%d'),
            'predicted_price': round(predicted_price, 2)
        })

        # Optionally, update X for next prediction
        # For a linear regression model, this may not be necessary

        # Save prediction to database
        StockPrediction.objects.update_or_create(
            symbol=SYMBOL,
            date=prediction_date,
            defaults={'predicted_price': predicted_price}
        )

    return JsonResponse({'predictions': predictions})
