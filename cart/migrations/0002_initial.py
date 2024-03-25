# Generated by Django 5.0.2 on 2024-03-24 23:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0001_initial'),
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='drinkcartitem',
            name='drink',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='delivery.drink'),
        ),
        migrations.AddField(
            model_name='drinkcartitem',
            name='drink_cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.drinkcart'),
        ),
        migrations.AddField(
            model_name='drinkcartitem',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cart.cartorder'),
        ),
        migrations.AddField(
            model_name='drinkcart',
            name='drinks',
            field=models.ManyToManyField(through='cart.DrinkCartItem', to='delivery.drink'),
        ),
        migrations.AddField(
            model_name='foodcartitem',
            name='food',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='delivery.food'),
        ),
        migrations.AddField(
            model_name='foodcartitem',
            name='food_cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.foodcart'),
        ),
        migrations.AddField(
            model_name='foodcartitem',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cart.cartorder'),
        ),
        migrations.AddField(
            model_name='foodcart',
            name='foods',
            field=models.ManyToManyField(through='cart.FoodCartItem', to='delivery.food'),
        ),
    ]
