from django.contrib import admin
from . import models

admin.site.register(models.FoodCart)
admin.site.register(models.FoodCartItem)
admin.site.register(models.DrinkCart)
admin.site.register(models.DrinkCartItem)
admin.site.register(models.CartOrder)
