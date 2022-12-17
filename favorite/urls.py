from django.urls import path, include
from .views import *


urlpatterns = [
    path('', favorite_info, name='list_favorite_prod'),
    path('add/<int:product_id>', favorite_add, name='add_favorite_prod'),
    path('remove/<int:product_id>', favorite_remove, name='remove_favorite_prod'),
    path('clear/', favorite_clear, name='clear_favorite_prod'),
]
