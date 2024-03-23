from django.shortcuts import render, redirect, get_object_or_404
from . import models, forms
from delivery.models import Food, Drink


def food_item_delete(request, pk):
    food = get_object_or_404(Food, id=pk)
    food_item = models.FoodCartItem.objects.filter(food=food).first()
    food_item.delete()
    return redirect('cart:view_cart')


def drink_item_delete(request, pk):
    drink = get_object_or_404(Drink, id=pk)
    drink_item = models.DrinkCartItem.objects.filter(drink=drink).first()
    drink_item.delete()
    return redirect('cart:view_cart')


def cart_view(request):
    session_key = request.session.session_key
    food_cart = models.FoodCart.objects.filter(session_key=session_key).first()
    drink_cart = models.DrinkCart.objects.filter(session_key=session_key).first()
    if request.method == "POST":
        form = forms.OrderForm(request.POST)
        if food_cart:
            for food_item in food_cart.foodcartitem_set.all():
                food_quantity = request.POST.get(f'quantity{food_item.food.pk}')
                request.session[f'quantity{food_item.food.pk}'] = food_quantity

        if drink_cart:
            for drink_item in drink_cart.drinkcartitem_set.all():
                drink_quantity = request.POST.get(f'quantity{drink_item.drink.pk}')
                request.session[f'quantity{drink_item.drink.pk}'] = drink_quantity

        return render(request, 'cart/order_create.html', {'form': form})

    if food_cart:
        foods_cart = food_cart.foods.all()
    else:
        foods_cart = []

    if drink_cart:
        drinks_cart = drink_cart.drinks.all()
    else:
        drinks_cart = []

    return render(request,
                  'cart/cart.html',
                  {'foods_cart': foods_cart,
                   'drinks_cart': drinks_cart})


def add_food(request, food_id):
    if request.method == 'POST':
        food = get_object_or_404(Food, id=food_id)

        session_key = request.session.session_key
        if not session_key:
            request.session.save()

        food_cart = models.FoodCart.objects.filter(session_key=session_key).first()

        if not food_cart:
            food_cart = models.FoodCart.objects.create(session_key=session_key)

        food_item, created = models.FoodCartItem.objects.get_or_create(food_cart=food_cart,
                                                                       food=food,
                                                                       quantity=1)

        if not created:
            food_item.quantity += 1
            food_item.save()
        else:
            food_item.quantity = 1
            food_item.save()

        food_cart.foods.add(food)

    return redirect('cart:view_cart')


def add_drink(request, drink_id):
    if request.method == 'POST':
        drink = get_object_or_404(Drink, id=drink_id)

        session_key = request.session.session_key
        if not session_key:
            request.session.save()

        drink_cart = models.DrinkCart.objects.filter(session_key=session_key).first()
        if not drink_cart:
            drink_cart = models.DrinkCart.objects.create(session_key=session_key)

        drink_item, created = models.DrinkCartItem.objects.get_or_create(drink_cart=drink_cart,
                                                                         drink=drink,
                                                                         quantity=1)
        if not created:
            drink_item.quantity += 1
            drink_item.save()
        else:
            drink_item.quantity = 1
            drink_item.save()

        drink_cart.drinks.add(drink)

        return redirect('cart:view_cart')


def checkout(request):
    if request.method == 'POST':
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            session_key = request.session.session_key

            food_cart = models.FoodCart.objects.filter(session_key=session_key).first()
            drink_cart = models.DrinkCart.objects.filter(session_key=session_key).first()

            total_price = 0
            if food_cart:
                for food_item in food_cart.foodcartitem_set.all():
                    food = food_item.food
                    food_item.quantity = request.session[f'quantity{food.pk}']
                    price = food.price * int(food_item.quantity)
                    total_price += price
                    order.total_price = total_price
                    order.save()

                    food_item.order = order
                    food_item.save()
                food_cart.delete()
            if drink_cart:
                for drink_item in drink_cart.drinkcartitem_set.all():
                    drink = drink_item.drink
                    drink_item.quantity = request.session[f'quantity{drink.pk}']
                    price = drink.price * int(drink_item.quantity)
                    total_price += price
                    order.total_price = total_price
                    order.save()

                    drink_item.order = order
                    drink_item.save()
                drink_cart.delete()

            order.save()
            total_price = order.total_price

            return render(request, 'cart/checkout.html', {'total_price': total_price})

        form = forms.OrderForm()
        return render(request, 'cart/order_create.html', {'form': form})
