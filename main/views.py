from urllib import request
from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .models import *
from .serializer import *
# Create your views here.

class SliderGET(APIView):
    def get(request):
        product = Product.objects.all().order_by('rating')[:5]
        ser = ProductSerializer(product, many=True)
        return Response(ser.data)

class Latest(APIView):
    def get(request):
        product = Product.objects.all().order_by('-id')[:6]
        ser = ProductSerializer(product, many=True)
        return Response(ser.data)

class NewletterPOST(APIView):
    def post(request):
        email = request.POST.get('email')
        news = Newsletter.objects.create(email=email)
        ser = NewsletterSerializer(news)
        return Response(ser.data)

class Search(APIView):
    def post(request):
        nam = request.POST.get('name')
        found = Product.objects.get(name__icontains=nam)
        ser = ProductSerializer(found,many=True)
        return Response(ser.data)

class Filter(APIView):
    def post(request):
        firstprice = int(request.POST.get('firstprice'))
        secondprice = int(request.POST.get('secondprice'))
        product = Product.objects.filter(price__gte=firstprice, price__lte=secondprice)
        ser = ProductSerializer(product, many=True)
        return Response(ser.data)

class Instock(APIView):
    def post(request):
        product = Product.objects.all()
        ser = ProductSerializer(product, many=True)
        if len(product)>=5:
            return Response(ser.data)
        else:
            return Response('No items in stock')

class Onsale(APIView):
    def post(request):
        product = Product.objects.filter(soldout=False)
        ser = ProductSerializer(product, many=True)
        return Response(ser.data)

