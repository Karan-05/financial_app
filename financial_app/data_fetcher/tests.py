# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse

class BacktestStrategyTest(TestCase):
    def setUp(self):
        # Set up initial data or mock data
        pass

    def test_backtest_strategy_default_parameters(self):
        client = Client()
        response = client.get(reverse('backtest_strategy'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('final_portfolio_value', response.json())

    def test_backtest_strategy_custom_parameters(self):
        client = Client()
        response = client.get(reverse('backtest_strategy'), {
            'initial_investment': '5000',
            'short_window': '30',
            'long_window': '100'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('final_portfolio_value', response.json())


# data_fetcher/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from .models import StockData
from datetime import datetime, timedelta

class BacktestStrategyTestCase(TestCase):
    def setUp(self):
        # Create sample data for testing
        symbol = 'AAPL'
        base_date = datetime.now().date() - timedelta(days=300)
        for i in range(250):
            date = base_date + timedelta(days=i)
            StockData.objects.create(
                symbol=symbol,
                date=date,
                open_price=100 + i * 0.1,
                high_price=100 + i * 0.2,
                low_price=100 + i * 0.05,
                close_price=100 + i * 0.15,
                volume=1000000 + i * 1000
            )
    
    def test_backtest_default_parameters(self):
        client = Client()
        response = client.get(reverse('backtest_strategy'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('initial_investment', data)
        self.assertIn('final_investment_value', data)
        self.assertIn('total_return', data)
        self.assertIn('total_return_percent', data)
        self.assertIn('max_drawdown_percent', data)
        self.assertIn('number_of_trades', data)
    
    def test_backtest_custom_parameters(self):
        client = Client()
        response = client.get(reverse('backtest_strategy'), {
            'initial_investment': '5000',
            'short_window': '5',
            'long_window': '20',
            'symbol': 'AAPL'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['initial_investment'], 5000.0)
        self.assertIn('final_investment_value', data)
        self.assertIn('total_return', data)
        self.assertIn('total_return_percent', data)
        self.assertIn('max_drawdown_percent', data)
        self.assertIn('number_of_trades', data)

    def test_backtest_invalid_parameters(self):
        client = Client()
        response = client.get(reverse('backtest_strategy'), {
            'initial_investment': 'abc',
            'short_window': '50',
            'long_window': '50',
        })
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)
    
    def test_backtest_no_data(self):
        # Test with a symbol that doesn't exist
        client = Client()
        response = client.get(reverse('backtest_strategy'), {
            'symbol': 'INVALID'
        })
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)
# data_fetcher/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from .models import StockData
from datetime import datetime, timedelta

class ReportGenerationTestCase(TestCase):
    def setUp(self):
        # Create sample data for testing
        symbol = 'AAPL'
        base_date = datetime.now().date() - timedelta(days=300)
        for i in range(250):
            date = base_date + timedelta(days=i)
            StockData.objects.create(
                symbol=symbol,
                date=date,
                open_price=100 + i * 0.1,
                high_price=100 + i * 0.2,
                low_price=100 + i * 0.05,
                close_price=100 + i * 0.15,
                volume=1000000 + i * 1000
            )
    
    def test_generate_pdf_report(self):
        client = Client()
        response = client.post(reverse('generate_report'), {
            'initial_investment': '10000',
            'short_window': '50',
            'long_window': '200',
            'symbol': 'AAPL',
            'output_format': 'pdf'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
    
    def test_generate_json_report(self):
        client = Client()
        response = client.post(reverse('generate_report'), {
            'initial_investment': '10000',
            'short_window': '50',
            'long_window': '200',
            'symbol': 'AAPL',
            'output_format': 'json'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = response.json()
        self.assertIn('result', data)
        self.assertIn('chart', data)
