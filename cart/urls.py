from django.urls import path
from . import views


app_name = 'cart'

urlpatterns = [
    path('cart/', views.cart_view, name='view_cart'),
    path('add/food/<int:food_id>/', views.add_food, name='add_food'),
    path('add/drink/<int:drink_id>/', views.add_drink, name='add_drink'),
    path('delete/food/<int:pk>/', views.food_item_delete, name='delete_food'),
    path('delete/drink/<int:pk>/', views.drink_item_delete, name='delete_drink'),
    path('cart/checkout/', views.checkout, name='checkout')
]
