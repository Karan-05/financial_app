# data_fetcher/utils.py

import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import base64
import pandas as pd

def create_stock_price_plot(dates, actual_prices, predicted_prices):
    # Convert dates to pandas datetime
    dates = pd.to_datetime(dates)

    plt.figure(figsize=(12, 6))
    plt.plot(dates, actual_prices, label='Actual Prices')
    plt.plot(dates, predicted_prices, label='Predicted Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Actual vs Predicted Stock Prices')
    plt.legend()

    # Improve the date axis
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))  # Set major ticks every 2 months
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Format date labels as Year-Month
    plt.gcf().autofmt_xdate()  # Auto-format date labels to prevent overlap

    plt.tight_layout()
    
    # Save the plot to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    
    # Encode the image to base64
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode('utf-8')
    buffer.close()
    
    return graph
