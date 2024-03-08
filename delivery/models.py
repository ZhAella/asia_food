import os
from django.db import models
from django.conf import settings


IMAGES_ROOT = os.path.relpath(os.path.join(settings.MEDIA_ROOT, 'images'))


class Food(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    weight = models.DecimalField(max_digits=3, decimal_places=2)
    photo = models.ImageField(upload_to=IMAGES_ROOT, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Drink(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    volume = models.DecimalField(max_digits=6, decimal_places=2)
    photo = models.ImageField(upload_to=IMAGES_ROOT, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    fio = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    def __str__(self):
        return f'Order to name {self.fio}'


class OrderFood(models.Model):
    food = models.ForeignKey(Food, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    def __str__(self):
        return f'Order: {self.food} Quantity:{self.quantity}'


class OrderDrink(models.Model):
    drink = models.ForeignKey(Drink, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    def __str__(self):
        return f'Order: {self.drink} Quantity:{self.quantity}'
