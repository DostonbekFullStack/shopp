from rest_framework import serializers
from .models import *

class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class Cardproductserializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['soldout', 'production', 'price', 'review', 'discount_price', 'date', 'rating']

class ProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Production
        fields = '__all__'


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Card
        fields = ['product', 'quantity']

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Purchase
        fields = '__all__'









