from . import models


def create_order(fio, address, phone_number, total_price):
    return models.Order.objects.create(
        fio=fio,
        address=address,
        phone_number=phone_number,
        total_price=total_price
    )


def create_order_food(food, order, quantity):
    price = food.price * int(quantity)

    return models.OrderFood(
        food=food,
        order=order,
        quantity=quantity,
        price=price
    )


def create_order_drink(drink, order, quantity):
    price = drink.price * int(quantity)

    return models.OrderDrink(
        drink=drink,
        order=order,
        quantity=quantity,
        price=price
    )
