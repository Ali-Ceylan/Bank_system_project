# Generated by Django 5.1.4 on 2025-01-11 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banka', '0013_alter_hesap_bakiye_paragonderme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hesap',
            name='bakiye',
            field=models.CharField(max_length=10),
        ),
    ]
