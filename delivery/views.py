from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)
from django.urls import reverse_lazy
from django.views import View
from . import models


class MenuView(ListView):
    model = models.Food
    template_name = 'delivery/menu.html'
    context_object_name = 'foods'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drinks'] = models.Drink.objects.all()
        return context


class FoodDetailView(DetailView):
    model = models.Food
    template_name = 'delivery/food.html'
    context_object_name = 'food'


class DrinkDetailView(DetailView):
    model = models.Drink
    template_name = 'delivery/drink.html'
    context_object_name = 'drink'


class FoodCreateView(CreateView):
    model = models.Food
    template_name = 'delivery/food_create.html'
    fields = ['name', 'price', 'weight', 'description', 'photo']
    success_url = reverse_lazy('menu')


class DrinkCreateView(CreateView):
    model = models.Drink
    template_name = 'delivery/drink_create.html'
    fields = ['name', 'price', 'volume', 'photo']
    success_url = reverse_lazy('menu')


class FoodUpdateView(UpdateView):
    model = models.Food
    template_name = 'delivery/food_update.html'
    fields = ['name', 'price', 'weight', 'description', 'photo']
    success_url = reverse_lazy('menu')


class DrinkUpdateView(UpdateView):
    model = models.Drink
    template_name = 'delivery/drink_update.html'
    fields = ['name', 'price', 'volume', 'photo']
    success_url = reverse_lazy('menu')


class FoodDeleteView(DeleteView):
    model = models.Food
    success_url = reverse_lazy('menu')


class DrinkDeleteView(DeleteView):
    model = models.Drink
    success_url = reverse_lazy('menu')


class CreateOrderView(View):
    drinks: tuple
    foods: tuple

    def get(self, request):
        self.foods = models.Food.objects.all()
        self.drinks = models.Drink.objects.all()
        return render(request,
                      'delivery/create_order.html',
                      {'foods': self.foods, 'drinks': self.drinks}
                      )
    @staticmethod
    def post(request):
        order = models.Order.objects.create(
            fio=request.POST['fio'],
            address=request.POST['address'],
            phone_number=request.POST['phone_number']
        )
        order.save()

        food_order = models.OrderFood.objects.create(
            food=get_object_or_404(models.Food, pk=request.POST['food']),
            food_quantity=request.POST['food_quantity'],
            order=order
        )
        food_order.save()

        drink_order = models.OrderDrink.objects.create(
            drink=get_object_or_404(models.Drink, pk=request.POST['drink']),
            drink_quantity=request.POST['drink_quantity'],
            order=order
        )
        drink_order.save()
        return redirect('/')


class OrdersListView(View):
    orders: tuple

    def get(self, request):
        self.orders = models.Order.objects.all()

        return render(request,
                      'delivery/orders_list.html',
                      {'orders': self.orders}
                      )


def order_products(request, pk):
    order = models.Order.objects.filter(pk=pk)
    foods = models.OrderFood.objects.get(order=order)
    drinks = get_object_or_404(models.OrderDrink, order=order)

    return render(request,
                  'delivery/order_products.html',
                  {
                      'order': order,
                      'food': foods,
                      'drink': drinks}
                  )

