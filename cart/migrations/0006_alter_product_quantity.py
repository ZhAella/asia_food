# Generated by Django 5.0.2 on 2024-03-18 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_order_cart_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(max_length=3),
        ),
    ]
