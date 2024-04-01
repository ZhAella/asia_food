from django.db import models
from delivery.models import Food, Drink


class CartOrder(models.Model):
    fio = models.CharField(max_length=100)
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=12)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now=True, auto_created=True, null=True)

    def __str__(self):
        return f'Order to {self.fio}'


class FoodCart(models.Model):
    foods = models.ManyToManyField(Food, through='FoodCartItem')
    session_key = models.CharField(max_length=40, null=True)


class FoodCartItem(models.Model):
    food_cart = models.ForeignKey(FoodCart, on_delete=models.SET_NULL, null=True)
    food = models.ForeignKey(Food, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(CartOrder, on_delete=models.DO_NOTHING, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.food} - {self.quantity} portion'


class DrinkCart(models.Model):
    drinks = models.ManyToManyField(Drink, through='DrinkCartItem')
    session_key = models.CharField(max_length=40, null=True)


class DrinkCartItem(models.Model):
    drink_cart = models.ForeignKey(DrinkCart, on_delete=models.SET_NULL, null=True)
    drink = models.ForeignKey(Drink, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(CartOrder, on_delete=models.DO_NOTHING, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.drink} - {self.quantity} portion'
