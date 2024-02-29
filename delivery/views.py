from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from . import models


class MenuView(View):
    foods: tuple
    drinks: tuple

    def get(self, request):
        self.foods = models.Food.objects.all()
        self.drinks = models.Drink.objects.all()
        return render(request,
                      'delivery/menu.html',
                      {'foods': self.foods, 'drinks': self.drinks}
                      )


class FoodDetailView(View):
    food: models.Food

    def get(self, request, pk):
        self.food = get_object_or_404(models.Food, pk=pk)
        return render(request,
                      'delivery/food.html',
                      {'food': self.food}
                      )


class DrinkDetailView(View):
    drink: models.Drink

    def get(self, request, pk):
        self.drink = get_object_or_404(models.Drink, pk=pk)
        return render(request,
                      'delivery/drink.html',
                      {'drink': self.drink}
                      )


class FoodCreateView(View):
    food: models.Food

    def get(self, request):
        self.food = models.Food.objects.all()
        return render(request,
                      'delivery/food_create.html',
                      {'food': self.food}
                      )

    def post(self, request):
        self.food = models.Food.objects.create(
            name=request.POST['name'],
            price=request.POST['price'],
            weight=request.POST['weight'],
            photo=request.FILES['photo'],
            description=request.POST['description']
        )
        self.food.save()
        return redirect('/')


class DrinkCreateView(View):
    drink: models.Drink

    def get(self, request):
        self.drink = models.Drink.objects.all()
        return render(request,
                      'delivery/drink_create.html',
                      {'drink': self.drink}
                      )

    def post(self, request):
        self.drink = models.Drink.objects.create(
            name=request.POST['name'],
            price=request.POST['price'],
            volume=request.POST['volume'],
            photo=request.FILES['photo'],
        )
        self.drink.save()
        return redirect('/')


class FoodUpdateView(View):
    food: models.Food

    def get(self, request, pk):
        self.food = get_object_or_404(models.Food, pk=pk)
        return render(request,
                      'delivery/food_update.html',
                      {'food': self.food})

    def post(self, request, pk):
        self.food = get_object_or_404(models.Food, pk=pk)
        self.food.name = request.POST['name']
        self.food.price = request.POST['price']
        self.food.weight = request.POST['weight']
        self.food.photo = request.FILES['photo']
        self.food.description = request.POST['description']
        self.food.save()
        return redirect('/')


class DrinkUpdateView(View):
    drink: models.Drink

    def get(self, request, pk):
        self.drink = get_object_or_404(models.Drink, pk=pk)
        return render(request,
                      'delivery/drink_update.html',
                      {'drink': self.drink})

    def post(self, request, pk):
        self.drink = get_object_or_404(models.Drink, pk=pk)
        self.drink.name = request.POST['name']
        self.drink.price = request.POST['price']
        self.drink.volume = request.POST['volume']
        self.drink.photo = request.FILES['photo']
        self.drink.save()
        return redirect('/')


class FoodDeleteView(View):
    food: models.Food

    def get(self, request, pk):
        self.food = get_object_or_404(models.Food, pk=pk)
        self.food.photo.delete()
        self.food.delete()
        return redirect('/')


class DrinkDeleteView(View):
    drink: models.Drink

    def get(self, request, pk):
        self.drink = get_object_or_404(models.Drink, pk=pk)
        self.drink.photo.delete()
        self.drink.delete()
        return redirect('/')


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

