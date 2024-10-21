from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Add this line for the root URL
    path('backtest/', views.backtest_strategy, name='backtest_strategy'),
    path('predict/', views.predict_stock_prices, name='predict_stock_prices'),
    path('report/', views.generate_report, name='generate_report'),
    path('backtest/', views.backtest_strategy, name='backtest_strategy'),
    path('generate_report/', views.generate_report, name='generate_report'),
]


