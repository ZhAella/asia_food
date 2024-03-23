from django.urls import path
from . import views

urlpatterns = [
    path('', views.MenuView.as_view(), name='menu'),
    path('sign_up', views.SignUpView.as_view(), name='sign_up'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('foods/<int:pk>', views.FoodDetailView.as_view(), name='food_detail'),
    path('drinks/<int:pk>', views.DrinkDetailView.as_view(), name='drink_detail'),
    path('foods/<int:pk>/update', views.FoodUpdateView.as_view(), name='food_update'),
    path('drinks/<int:pk>/update', views.DrinkUpdateView.as_view(), name='drink_update'),
    path('foods/<int:pk>/delete', views.FoodDeleteView.as_view(), name='food_delete'),
    path('drinks/<int:pk>/delete', views.DrinkDeleteView.as_view(), name='drink_delete'),
    path('make_order', views.OrderCreateView.as_view(), name='create_order'),
    path('make_order/products', views.OrderProductsCreateView.as_view(), name='ordered_products'),
    path('orders_list', views.OrderListView.as_view(), name='orders_list'),
    path('orders_list/<int:pk>', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders_list/<int:pk>/', views.CartOrderDetailView.as_view(), name='cart_order_detail'),
    path('food_create', views.FoodCreateView.as_view(), name='food_create'),
    path('drink_create', views.DrinkCreateView.as_view(), name='drink_create')
]
