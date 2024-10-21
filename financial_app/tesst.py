# test_api.py

import requests
from decouple import config

API_KEY = config('ALPHA_VANTAGE_API_KEY')

SYMBOL = 'IBM'
FUNCTION = 'TIME_SERIES_DAILY'
URL = 'https://www.alphavantage.co/query'

params = {
    'function': FUNCTION,
    'symbol': SYMBOL,
    'outputsize': 'compact',
    'apikey': API_KEY
}

response = requests.get(URL, params=params)
data = response.json()

print(data)
