from django.urls import path
from . import views

urlpatterns = [
    path('', views.MenuView.as_view(), name='menu'),
    path('foods/<int:pk>', views.FoodDetailView.as_view(), name='food_detail'),
    path('drinks/<int:pk>', views.DrinkDetailView.as_view(), name='drink_detail'),
    path('foods/<int:pk>/update', views.FoodUpdateView.as_view(), name='food_update'),
    path('drinks/<int:pk>/update', views.DrinkUpdateView.as_view(), name='drink_update'),
    path('foods/<int:pk>/delete', views.FoodDeleteView.as_view(), name='food_delete'),
    path('drinks/<int:pk>/delete', views.DrinkDeleteView.as_view(), name='drink_delete'),
    path('make_order', views.CreateOrderView.as_view(), name='create_order'),
    path('orders_list', views.OrdersListView.as_view(), name='orders_list'),
    path('orders_list/<int:pk>', views.order_products, name='order_products')
]
