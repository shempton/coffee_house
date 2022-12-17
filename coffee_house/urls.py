from django.urls import path

from . import views

urlpatterns = [
    # Coffee
    path('', views.CoffeeList.as_view(), name='coffee_list'),
    path('<int:pk>/', views.CoffeeDetail.as_view(), name='coffee_detail'),
    path('add-coffee/', views.CoffeeCreate.as_view(), name='coffee_create'),
    path('upd-coffee/<int:pk>/', views.CoffeeUpdate.as_view(), name='coffee_update'),
    path('coffee/delete/<int:pk>/', views.CoffeeDelete.as_view(), name='coffee_delete'),

    path('delete-ingcoffee/<int:pk>/', views.delete_ingcoffee, name='delete_ingcoffee'),
    path('delete-recipe/<int:pk>/', views.delete_recipe, name='delete_recipe'),

    # Ingredients
    path('ingredients/', views.IngredientList.as_view(), name='ingredient_list'),
    path('ingredients/<int:pk>/', views.IngredientDetail.as_view(), name='ingredient_detail'),
    path('ingredients/create/', views.IngredientCreate.as_view(), name='ingredient_create'),
    path('ingredients/update/<int:pk>', views.IngredientUpdate.as_view(), name='ingredient_update'),
    path('ingredients/delete/<int:pk>', views.IngredientDelete.as_view(), name='ingredient_delete'),

    # Registration and auth
    path('registration/', views.user_registration, name='regis'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('contact/', views.contact_email, name='contact_email'),

    path('api/coffee/', views.coffee_api_list, name='api_coffee_list'),
    path('api/coffee/<int:pk>', views.coffee_api_detail, name='api_coffee_detail'),

]
