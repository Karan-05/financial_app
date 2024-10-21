from django.db import models

# Create your models here.
class StockData(models.Model):
    symbol = models.CharField(max_length=10)
    date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ('symbol', 'date')
        ordering = ['date']

    def __str__(self):
        return f"{self.symbol} - {self.date}"

class StockPrediction(models.Model):
    symbol = models.CharField(max_length=10)
    date = models.DateField()
    predicted_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('symbol', 'date')
        ordering = ['date']

    def __str__(self):
        return f"{self.symbol} Prediction - {self.date}"


# data_fetcher/models.py

from django.db import models

class StockData(models.Model):
    symbol = models.CharField(max_length=10)
    date = models.DateField()
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ('symbol', 'date')
        ordering = ['date']

    def __str__(self):
        return f"{self.symbol} - {self.date}"
