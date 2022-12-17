from django.shortcuts import render, redirect, get_object_or_404
from coffee_house.models import coffee
from .favorite import Favorite
from django.views.decorators.http import require_POST


@require_POST
def favorite_add(request, product_id):
    favorite = Favorite(request)
    product_obj = get_object_or_404(coffee, pk=product_id)

    favorite.add(product=product_obj)

    return redirect(request.META.get('HTTP_REFERER'))


def favorite_remove(request, product_id):
    favorite = Favorite(request)
    product_obj = get_object_or_404(coffee, pk=product_id)

    favorite.remove(product_obj)
    return redirect(request.META.get('HTTP_REFERER'))


def favorite_info(request):
    favorite = Favorite(request)
    return render(request, 'favorite/detail.html', {'favorite': favorite})


def favorite_clear(request):
    favorite = Favorite(request)
    favorite.clear()
    return redirect('coffee_list')
