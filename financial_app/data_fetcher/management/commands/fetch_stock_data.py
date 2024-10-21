# data_fetcher/management/commands/fetch_stock_data.py

import requests
from django.core.management.base import BaseCommand
from data_fetcher.models import StockData
from datetime import datetime, timedelta
from django.db import IntegrityError
import traceback
import time
from decouple import config
import logging

class Command(BaseCommand):
    help = 'Fetch stock data from Alpha Vantage API'

    def handle(self, *args, **options):
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        logger.info('Starting data fetch...')

        # Get API key from environment variable or .env file
        API_KEY = config('ALPHA_VANTAGE_API_KEY', default='YOUR_ALPHA_VANTAGE_API_KEY')
        if API_KEY == 'YOUR_ALPHA_VANTAGE_API_KEY':
            logger.error('API key not set. Please set ALPHA_VANTAGE_API_KEY in your environment or .env file.')
            return

        SYMBOL = 'AAPL'
        FUNCTION = 'TIME_SERIES_DAILY'
        URL = 'https://www.alphavantage.co/query'

        params = {
            'function': FUNCTION,
            'symbol': SYMBOL,
            'outputsize': 'full',  # Use 'compact' to avoid premium limitations
            'apikey': API_KEY
        }

        try:
            response = requests.get(URL, params=params)
            response.raise_for_status()
            logger.info('API response received.')
        except requests.RequestException as e:
            logger.error(f"Network error: {e}")
            return

        data = response.json()

        # Handle API errors
        if "Note" in data:
            logger.error("API call frequency is too high. Please wait and try again.")
            return
        if "Error Message" in data:
            logger.error(f"Error fetching data: {data['Error Message']}")
            return
        if "Information" in data:
            logger.error(f"Information: {data['Information']}")
            return

        time_series_key = 'Time Series (Daily)'
        time_series = data.get(time_series_key)
        if not time_series:
            logger.error(f"No '{time_series_key}' found in API response.")
            return

        logger.info('Processing time series data...')

        # Prepare date limit (2 years ago)
        two_years_ago = datetime.now() - timedelta(days=730)

        for date_str, daily_data in time_series.items():
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError as e:
                logger.error(f"Date parsing error for {date_str}: {e}")
                continue

            # Skip future dates
            if date > datetime.now().date():
                logger.warning(f"Skipping future date: {date}")
                continue

            # Skip data older than two years
            if date < two_years_ago.date():
                continue

            logger.info(f"Processing data for {date}")

            # Map API data to model fields
            field_mappings = {
                'open_price': '1. open',
                'high_price': '2. high',
                'low_price': '3. low',
                'close_price': '4. close',
                'volume': '5. volume'  # Adjusted key for TIME_SERIES_DAILY
            }

            # Prepare defaults dictionary
            defaults = {}
            missing_fields = []
            for field, key in field_mappings.items():
                value = daily_data.get(key)
                if value is not None:
                    # Convert string values to appropriate types
                    if field == 'volume':
                        defaults[field] = int(float(value))
                    else:
                        defaults[field] = float(value)
                else:
                    missing_fields.append(key)

            if missing_fields:
                logger.warning(f"Missing data for {date}: {missing_fields}")
                continue  # Skip this date or handle accordingly

            try:
                stock_data, created = StockData.objects.update_or_create(
                    symbol=SYMBOL,
                    date=date,
                    defaults=defaults
                )
                if created:
                    logger.info(f"Data for {date} created successfully.")
                else:
                    logger.info(f"Data for {date} updated successfully.")
            except Exception as e:
                logger.error(f"Error saving data for {date}: {e}")
                traceback.print_exc()
                continue

        logger.info('Successfully fetched and stored stock data.')
