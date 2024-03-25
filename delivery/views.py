from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView, TemplateView)
from django.urls import reverse_lazy
from django.views import View
from . import models, utils, forms
from cart.models import CartOrder


class SignUpView(CreateView):
    model = models.CustomerUser
    template_name = 'delivery/sign_up.html'
    form_class = forms.CustomerUserForm
    success_url = reverse_lazy('menu')


def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect('menu')

    return render(request, 'delivery/sign_in.html')


def log_out(request):
    logout(request)
    return redirect('')


class MenuView(ListView):
    model = models.FoodType
    template_name = 'delivery/menu.html'
    context_object_name = 'food_types'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        food_types = context['food_types']
        foods_by_type = {}
        for food_type in food_types:
            foods_by_type[food_type] = food_type.food_set.all()
        context['foods_by_type'] = foods_by_type
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

    def form_valid(self, form):
        food_type = form.cleaned_data['type']
        new_food_type = form.cleaned_data['new_food_type']
        if new_food_type:
            food_type = models.FoodType.objects.create(name=new_food_type)
        form.instance.type = food_type

        return super().form_valid(form)


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

    @login_required
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.OrderForm()
        return context

    @login_required
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
    @login_required
    def get(request):
        foods = models.Food.objects.all()
        drinks = models.Drink.objects.all()
        return render(request,
                      'delivery/ordered_products.html',
                      {'foods': foods, 'drinks': drinks}
                      )

    @staticmethod
    @login_required
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_orders'] = CartOrder.objects.all()
        return context


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
        context['total_price'] = order.total_price
        return context


class CartOrderDetailView(DetailView):
    models = CartOrder
    queryset = CartOrder.objects.all()
    template_name = 'delivery/orders_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_order = self.get_object()
        foods_item = cart_order.foodcartitem_set.all()
        drinks_item = cart_order.drinkcartitem_set.all()
        context['foods_item'] = foods_item
        context['drinks_item'] = drinks_item
        context['total_price'] = cart_order.total_price
        return context
