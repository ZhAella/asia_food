# Generated by Django 5.0.2 on 2024-03-22 00:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0017_remove_drinkcart_order_remove_foodcart_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drinkcartitem',
            name='drink_cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.drinkcart'),
        ),
        migrations.AlterField(
            model_name='foodcartitem',
            name='food_cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.foodcart'),
        ),
    ]
