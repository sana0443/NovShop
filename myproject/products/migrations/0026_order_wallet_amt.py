# Generated by Django 4.1.5 on 2023-03-11 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_alter_wallet_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='wallet_amt',
            field=models.FloatField(null=True),
        ),
    ]