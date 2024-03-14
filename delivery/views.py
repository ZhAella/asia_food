from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView, TemplateView)
from django.urls import reverse_lazy
from django.views import View
from . import models, utils, forms


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
    form_class = forms.FoodForm
    success_url = reverse_lazy('menu')


class DrinkCreateView(CreateView):
    model = models.Drink
    template_name = 'delivery/drink_create.html'
    form_class = forms.DrinkForm
    success_url = reverse_lazy('menu')


class FoodUpdateView(UpdateView):
    model = models.Food
    template_name = 'delivery/food_update.html'
    form_class = forms.FoodForm
    success_url = reverse_lazy('menu')


class DrinkUpdateView(UpdateView):
    model = models.Drink
    template_name = 'delivery/drink_update.html'
    form_class = forms.DrinkForm
    success_url = reverse_lazy('menu')


class FoodDeleteView(DeleteView):
    model = models.Food
    success_url = reverse_lazy('menu')


class DrinkDeleteView(DeleteView):
    model = models.Drink
    success_url = reverse_lazy('menu')


class OrderCreateView(TemplateView):
    template_name = 'delivery/create_order.html'

    def post(self, request):
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            request.session['fio'] = form.cleaned_data['fio']
            request.session['address'] = form.cleaned_data['address']
            request.session['phone_number'] = form.cleaned_data['phone_number']
            return redirect('ordered_products')

        return render(request, self.template_name, {'form': form})


class OrderProductsCreateView(View):
    @staticmethod
    def get(request):
        foods = models.Food.objects.all()
        drinks = models.Drink.objects.all()
        return render(request,
                      'delivery/ordered_products.html',
                      {'foods': foods, 'drinks': drinks}
                      )

    @staticmethod
    def post(request):
        food_ids = request.POST.getlist('foods')
        drink_ids = request.POST.getlist('drinks')
        order = utils.create_order(request.session['fio'],
                                   request.session['address'],
                                   request.session['phone_number'],
                                   0)
        total_price = 0

        for food_id in food_ids:
            food = get_object_or_404(models.Food, id=food_id)
            order_food = utils.create_order_food(food, order,
                                                 request.POST[f'quantity{food_id}'])
            total_price += order_food.price
            order_food.save()

        for drink_id in drink_ids:
            drink = get_object_or_404(models.Drink, id=drink_id)
            order_drink = utils.create_order_drink(drink, order,
                                                   request.POST[f'quantity{drink_id}'])
            total_price += order_drink.price
            order_drink.save()

        order.total_price = total_price
        order.save()

        return redirect('menu')


class OrderListView(ListView):
    model = models.Order
    template_name = 'delivery/orders_list.html'
    context_object_name = 'orders'


class OrderDetailView(DetailView):
    model = models.Order
    template_name = 'delivery/orders_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        order_foods = order.orderfood_set.all()
        order_drinks = order.orderdrink_set.all()
        context['order_foods'] = order_foods
        context['order_drinks'] = order_drinks
        return context
