from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import BadRequest, PermissionDenied

from django.http import HttpResponse, HttpResponseRedirect
from .models import coffee, recipe_coffee, ingredient_coffee, ingredients
from .forms import RegistrationForm, LoginForm, ContactForm, CoffeeForm, IngCoffeeFormSet, RecipeCoffeeFormSet, \
    IngredientForm

from django.core.paginator import Paginator
from django.contrib.auth import login, logout

from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

from django.core.mail import send_mail
from django.conf import settings

from django.contrib import messages

from django.urls import reverse_lazy

# API
from .serializer import CoffeeSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# VIEWS
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class CoffeeList(ListView):
    model = coffee
    template_name = 'coffee_house/coffee/coffee_list_class.html'
    extra_context = {'title': 'Главная'}

    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['keys_favorite'] = get_favorite_keys_from_session(self.request)
        context['keys_basket'] = get_basket_keys_from_session(self.request)
        return context

    def get_queryset(self):
        return coffee.objects.filter(exists=True).order_by('name')


def get_favorite_keys_from_session(request):
    if request.session.get('favorite'):
        favorite = request.session.get('favorite')
        list_keys = []
        for key, value in favorite.items():
            list_keys.append(key)

        return list(map(int, list_keys))
    else:
        return []


def get_basket_keys_from_session(request):
    if request.session.get('basket'):
        basket = request.session.get('basket')
        list_keys = []
        for key, value in basket.items():
            list_keys.append(key)

        return list(map(int, list_keys))
    else:
        return []


class CoffeeDetail(DetailView):
    model = coffee
    template_name = 'coffee_house/coffee/coffee_detail_class.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = recipe_coffee.objects.filter(coffee=self.object).order_by('step')
        context['cof_ing'] = ingredient_coffee.objects.filter(coffee=self.object)
        context['keys_favorite'] = get_favorite_keys_from_session(self.request)
        context['keys_basket'] = get_basket_keys_from_session(self.request)
        return context


class CoffeeInline():
    form_class = CoffeeForm
    model = coffee
    template_name = 'coffee_house/coffee/coffee_add.html'

    def form_valid(self, form):

        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('coffee_detail', self.object.pk)

    def formset_ingcoffee_valid(self, formset):
        ing_coffee = formset.save(commit=False)

        for obj in formset.deleted_objects:
            obj.delete()
        for variant in ing_coffee:
            variant.coffee = self.object
            variant.save()

    def formset_recipe_valid(self, formset):
        recipe = formset.save(commit=False)

        for obj in formset.deleted_objects:
            obj.delete()
        for rec in recipe:
            rec.coffee = self.object
            rec.save()


class CoffeeCreate(CoffeeInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(CoffeeCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'ingcoffee': IngCoffeeFormSet(prefix='ingcoffee'),
                'recipe': RecipeCoffeeFormSet(prefix='recipe'),
            }
        else:
            return {
                'ingcoffee': IngCoffeeFormSet(self.request.POST or None, self.request.FILES or None,
                                              prefix='ingcoffee'),
                'recipe': RecipeCoffeeFormSet(self.request.POST or None, self.request.FILES or None,
                                              prefix='recipe'),
            }

    @method_decorator(permission_required('coffee.add_coffee'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CoffeeUpdate(CoffeeInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(CoffeeUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'ingcoffee': IngCoffeeFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object,
                                          prefix='ingcoffee'),
            'recipe': RecipeCoffeeFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object,
                                          prefix='recipe'),
        }

    @method_decorator(permission_required('coffee.change_coffee'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def delete_ingcoffee(request, pk):
    try:
        variant = ingredient_coffee.objects.get(id=pk)
    except ingredient_coffee.DoesNotExist:
        messages.success(
            request, 'Такого объекта не существует'
        )
        return redirect('coffee_update', pk=variant.coffee.id)

    variant.delete()
    messages.success(
        request, 'Успешно удалено'
    )
    return redirect('coffee_update', pk=variant.coffee.id)


def delete_recipe(request, pk):
    try:
        variant = recipe_coffee.objects.get(id=pk)
    except recipe_coffee.DoesNotExist:
        messages.success(
            request, 'Такого объекта не существует'
        )
        return redirect('coffee_update', pk=variant.coffee.id)

    variant.delete()
    messages.success(
        request, 'Успешно удалено'
    )
    return redirect('coffee_update', pk=variant.coffee.id)


class CoffeeDelete(DeleteView):
    model = coffee
    template_name = 'coffee_house/coffee/coffee_delete.html'
    success_url = reverse_lazy('coffee_list')

    @method_decorator(permission_required('coffee.delete_coffee'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class IngredientList(ListView):
    model = ingredients
    template_name = 'coffee_house/ingredients/ing_list.html'
    extra_context = {'title': 'Ингредиенты'}

    paginate_by = 12

    def get_queryset(self):
        return ingredients.objects.filter(exists=True).order_by('name')


class IngredientDetail(DetailView):
    model = ingredients
    template_name = 'coffee_house/ingredients/ing_detail.html'


class IngredientCreate(CreateView):
    model = ingredients
    form_class = IngredientForm
    template_name = 'coffee_house/ingredients/ing_add.html'
    success_url = reverse_lazy('ingredient_list')

    @method_decorator(permission_required('ingredients.add_ingredients'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class IngredientUpdate(UpdateView):
    model = ingredients
    form_class = IngredientForm
    template_name = 'coffee_house/ingredients/ing_add.html'

    @method_decorator(permission_required('ingredients.change_ingredients'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class IngredientDelete(DeleteView):
    model = ingredients
    template_name = 'coffee_house/ingredients/ing_delete.html'
    success_url = reverse_lazy('ingredient_list')

    @method_decorator(permission_required('ingredients.delete_ingredients'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def user_registration(request):
    if request.user.is_authenticated:
        return error_404(request, 'e')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('coffee_list')
    else:
        form = RegistrationForm()
    return render(request, 'auth/registration.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return error_404(request, 'e')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('coffee_list')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})


def user_logout(request):
    if request.user.is_anonymous:
        return error_404(request, 'e')
    logout(request)
    return redirect('login')


@api_view(['GET', 'POST'])
@permission_required('coffee.add_coffee')
def coffee_api_list(request):
    if request.method == 'GET':
        coffee_list = coffee.objects.all()
        serializer = CoffeeSerializer(coffee_list, many=True)
        return Response({'coffee': serializer.data})
    elif request.method == 'POST':
        serializer = CoffeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_required(['coffee.change_coffee', 'coffee.delete_coffee'])
def coffee_api_detail(request, pk):
    coffee_obj = get_object_or_404(coffee, pk=pk)

    if request.method == 'GET':
        serializer = CoffeeSerializer(coffee_obj)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CoffeeSerializer(coffee_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        coffee_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def error_404(request, exception):
    response = render(request, 'errors/404.html', {'title': 'Страница не найдена'})
    response.status_code = 404
    return response


def error_400(request, exception):
    response = render(request, 'errors/400.html', {'title': 'Неверный запрос'})
    response.status_code = 400
    return response


def error_403(request, exception):
    response = render(request, 'errors/403.html', {'title': 'Ошибка доступа'})
    response.status_code = 403
    return response


def error_500(request, *args, **kwargs):
    response = render(request, 'errors/500.html', {'title': 'Внутренняя ошибка сервера'})
    response.status_code = 500
    return response
