from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import *


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):
    # groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'name', 'url')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'url', 'urlToBuy',
                  'priceStart', 'priceCurrent', 'priceHighest', 'priceLowest',
                  'dateAdded', 'dateLastChecked', 'dateHighest', 'dateLowest',
                  'store_id', 'is_active')


class ConnectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connector
        fields = ('id', 'user_id', 'product_id', 'is_active')
