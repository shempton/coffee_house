from django.contrib import admin

from .models import coffee, ingredients, ingredient_coffee, recipe_coffee


class CoffeeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'volume', 'price', 'exists', 'update_date')
    list_display_links = ('name',)
    search_fields = ('name', 'price')
    list_editable = ('volume', 'price', 'exists')
    list_filter = ('exists',)


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'exists', 'update_date')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_editable = ('price', 'exists')
    list_filter = ('exists',)


admin.site.register(coffee, CoffeeAdmin)
admin.site.register(ingredients, IngredientsAdmin)
admin.site.register(ingredient_coffee)
admin.site.register(recipe_coffee)
