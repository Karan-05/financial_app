# Generated by Django 3.2.25 on 2024-10-20 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_fetcher', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockPrediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=10)),
                ('date', models.DateField()),
                ('predicted_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'ordering': ['date'],
                'unique_together': {('symbol', 'date')},
            },
        ),
    ]