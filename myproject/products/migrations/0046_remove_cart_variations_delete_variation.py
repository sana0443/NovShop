# Generated by Django 4.1.7 on 2023-10-26 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0045_delete_coupen_remove_orderitem_order_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='variations',
        ),
        migrations.DeleteModel(
            name='variation',
        ),
    ]
