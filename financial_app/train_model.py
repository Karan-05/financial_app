# train_model.py

import os
import sys

# Set up Django environment
# Add the project directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'financial_app.settings')

import django
django.setup()

from django.conf import settings
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

from data_fetcher.models import StockData

# Fetch historical data from the database
qs = StockData.objects.filter(symbol='AAPL').order_by('date')
if not qs.exists():
    print("No historical data available to train the model.")
    sys.exit()

data = pd.DataFrame.from_records(qs.values())
print(data)

# Prepare features and target variable
data['target'] = data['close_price'].shift(-1)
data = data.dropna()

features = data[['open_price', 'high_price', 'low_price', 'close_price', 'volume']]
target = data['target']

# Train the model
model = LinearRegression()
model.fit(features, target)

# Save the model
MODEL_DIR = os.path.join(settings.BASE_DIR, 'models')
os.makedirs(MODEL_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODEL_DIR, 'stock_prediction_model.pkl')
joblib.dump(model, MODEL_PATH)

print(f"Model saved to {MODEL_PATH}")
