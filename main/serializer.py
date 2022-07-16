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

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'











