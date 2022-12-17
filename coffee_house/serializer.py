# API
from rest_framework import serializers
from .models import coffee


class CoffeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = coffee
        fields = ['pk', 'name', 'volume', 'description', 'price', 'exists']

