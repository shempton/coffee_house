from django.conf import settings
from coffee_house.models import coffee


class Favorite:

    def __init__(self, request):
        self.session = request.session
        favorite = self.session.get(settings.FAVORITE_SESSION_ID)
        if not favorite:
            favorite = self.session[settings.FAVORITE_SESSION_ID] = {}
        self.favorite = favorite

    def save(self):
        self.session[settings.FAVORITE_SESSION_ID] = self.favorite
        self.session.modified = True

    def add(self, product):
        prod_pk = str(product.pk)

        if prod_pk not in self.favorite:
            self.favorite[prod_pk] = {
                'price_prod': str(product.price)
            }

        self.save()

    def remove(self, product):
        prod_pk = str(product.pk)

        if prod_pk in self.favorite:
            del self.favorite[prod_pk]
            self.save()

    def clear(self):
        del self.session[settings.FAVORITE_SESSION_ID]
        self.session.modified = True

    def __iter__(self):
        list_prod_pk = self.favorite.keys()

        list_prod_obj = coffee.objects.filter(pk__in=list_prod_pk)

        favorite = self.favorite.copy()
        for prod_obj in list_prod_obj:
            favorite[str(prod_obj.pk)]['coffee'] = prod_obj

        for item in favorite.values():
            yield item
