from django import forms
from .models import coffee, recipe_coffee, ingredient_coffee, ingredients
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError


class CoffeeForm(forms.ModelForm):
    class Meta:
        model = coffee
        fields = ('name', 'volume', 'price', 'description', 'photo', 'ingredient')
        exclude = ['ingredient']

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'volume': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

    def clean_volume(self):
        volume = self.cleaned_data['volume']
        if volume < 0:
            raise ValidationError('Объем должен быть больше нуля')
        return volume

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError('Стоимость не может быть меньше нуля')
        return price


class IngCoffeeForm(forms.ModelForm):
    class Meta:
        model = ingredient_coffee
        fields = '__all__'


class RecipeCoffeeForm(forms.ModelForm):
    class Meta:
        model = recipe_coffee
        fields = '__all__'


IngCoffeeFormSet = inlineformset_factory(coffee, ingredient_coffee, form=IngCoffeeForm, extra=1,
                                         can_delete=True, can_delete_extra=True)

RecipeCoffeeFormSet = inlineformset_factory(coffee, recipe_coffee, form=RecipeCoffeeForm, extra=1,
                                            can_delete=True, can_delete_extra=True)


class IngredientForm(forms.ModelForm):
    class Meta:
        model = ingredients
        fields = ('name', 'description', 'price', 'photo')

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError('Стоимость не может быть меньше нуля')
        return price


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Логин пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
        min_length=2,
    )
    password1 = forms.CharField(
        label='Введите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
        min_length=2,
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )


class ContactForm(forms.Form):
    subject = forms.CharField(
        label='Заголовок письма',
        widget=forms.TextInput(
            attrs={'class': 'form-control'},
        ),
    )
    content = forms.CharField(
        label='Текст письма',
        widget=forms.Textarea(
            attrs={'class': 'form-control',
                   'rows': 7, }
        )
    )
