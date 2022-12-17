from django.shortcuts import render, redirect, get_object_or_404
from coffee_house.models import coffee
from .basket import Basket
from django.views.decorators.http import require_POST


@require_POST
def basket_add(request, product_id):
    basket = Basket(request)

    product_obj = get_object_or_404(coffee, pk=product_id)

    basket.add(product=product_obj)

    return redirect(request.META.get('HTTP_REFERER'))


@require_POST
def basket_update(request, product_id):
    basket = Basket(request)

    product_obj = get_object_or_404(coffee, pk=product_id)

    if request.POST['quantity']:
        quantity = request.POST['quantity']
        basket.add(product=product_obj, count_product=quantity)

    return redirect('list_basket_prod')


def basket_remove(request, product_id):
    basket = Basket(request)
    product_obj = get_object_or_404(coffee, pk=product_id)

    basket.remove(product_obj)
    return redirect('list_basket_prod')


def basket_info(request):
    basket = Basket(request)
    return render(request, 'basket/detail.html', {'basket': basket})


def basket_clear(request):
    basket = Basket(request)
    basket.clear()
    return redirect('coffee_list')
