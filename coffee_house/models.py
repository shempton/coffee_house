from django.db import models
from django.urls import reverse


class ingredients(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    photo = models.ImageField(upload_to='image/ingredients/%Y/%m/%d', blank=True, null=True, verbose_name='Картинка')
    price = models.FloatField(verbose_name='Цена')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления записи')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')
    exists = models.BooleanField(default=True, verbose_name='Существует ли?')

    def get_absolute_url(self):
        return reverse('ingredient_detail', kwargs={'pk': self.pk})

    def delete(self, using=None, keep_parents=False):
        obj = ingredients.objects.get(pk=self.pk)
        obj.exists = False
        obj.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name', '-price']


class coffee(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    volume = models.FloatField(verbose_name='Объем в мл')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    photo = models.ImageField(upload_to='image/%Y/%m/%d', blank=True, null=True, verbose_name='Картинка')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления записи')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')
    exists = models.BooleanField(default=True, verbose_name='Существует ли?')

    ingredient = models.ManyToManyField(ingredients, through='ingredient_coffee', verbose_name='Ингредиент')

    def get_absolute_url(self):
        return reverse('coffee_detail', kwargs={'pk': self.pk})

    def delete(self, using=None, keep_parents=False):
        obj = coffee.objects.get(pk=self.pk)
        obj.exists = False
        obj.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Кофе'
        verbose_name_plural = 'Кофе'
        ordering = ['name', '-price']


class ingredient_coffee(models.Model):
    coffee = models.ForeignKey(coffee, on_delete=models.CASCADE, verbose_name='Кофе')
    ingredient = models.ForeignKey(ingredients, on_delete=models.CASCADE, verbose_name='Ингредиент')
    count_ingredient = models.FloatField(verbose_name='Кол-во')
    measured = models.CharField(max_length=50, verbose_name='В чем измеряется?')

    def __str__(self):
        return self.coffee.__str__() + " содержит " + str(self.count_ingredient) + " " + \
               str(self.measured) + " " + self.ingredient.__str__()

    class Meta:
        verbose_name = 'Ингредиент кофе'
        verbose_name_plural = 'Ингредиенты кофе'
        unique_together = [['coffee', 'ingredient']]


class recipe_coffee(models.Model):
    step = models.IntegerField(verbose_name='Шаг')
    description = models.TextField(blank=False, verbose_name='Описание')
    photo = models.ImageField(upload_to='image/recipe/%Y/%m/%d', blank=True, null=True, verbose_name='Картинка')

    coffee = models.ForeignKey(coffee, on_delete=models.CASCADE, verbose_name='Кофе')

    def __str__(self):
        return self.coffee.__str__() + ' | ' + str(self.step) + ' - ' + self.description

    class Meta:
        verbose_name = 'Рецепт кофе'
        verbose_name_plural = 'Рецепты кофе'
