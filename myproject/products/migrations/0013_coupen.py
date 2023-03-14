# Generated by Django 4.1.5 on 2023-02-24 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_wishlist_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='coupen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('discount', models.FloatField()),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('active', models.BooleanField()),
            ],
        ),
    ]