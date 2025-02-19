# Generated by Django 5.1.4 on 2025-01-16 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banka', '0017_islem'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_type', models.CharField(max_length=50, unique=True)),
                ('value', models.DecimalField(decimal_places=4, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
