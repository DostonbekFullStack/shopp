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


class ProductPk(APIView):
    def get(request, pk):
        product = Product.objects.get(id=pk)
        ser = ProductSerializer(product)
        return Response(ser.data)

class ProductView(APIView):
    def get(self, request):
        product = Product.objects.all()
        ser = ProductSerializer(product, many=True)
        return Response(ser.data)
    
    def post(self, request, pk):
        a = Production.objects.get(id=pk)
        quantity = int(request.POST.get('quantity'))
        if quantity > a.quantity:
            return Response('error quantity')
        else:
            b = a.quantity - quantity
            a.quantity = b
            print(a.quantity)
            a.save()
            myquantity = quantity
        price = float(request.POST.get('price'))
        discount_price = int(request.POST.get('discount'))
        if discount_price > 0:
            myprice = price - (price * discount_price / 100)
            b = Product.objects.create(product_id=a.id, price=myprice,quantity=myquantity, discount_price=discount_price)
            ser = ProductSerializer(b)
            return Response(ser.data)
        else:
            Product.objects.create(product_id=a.id, price=price,quantity=myquantity)
            return Response(ser.data)

class ProductionView(APIView):
    def post(request):
        category = request.POST.get('category')
        image = request.FILES('image')
        image2 = request.FILES('image2')
        image3 = request.FILES('image3')
        image4 = request.FILES('image4')
        image5 = request.FILES('image5')
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        sku = request.POST.get('sku')
        description = request.POST.get('description')
        weight = request.POST.get('weight')
        dimentions = request.POST.get('dimentions')
        material = request.POST.get('material')
        Production.objects.create(category_id=category,image=image,image2=image2,image3=image3,
        image4=image4,image5=image5,name=name,quantity=quantity,sku=sku,description=description,
        weight=weight,dimentions=dimentions,material=material)

class CardView(APIView):
    def get(request, pk):
        card = Card.objects.get(user_id=pk)
        ser = CardSerializer(card)
        return Response(ser.data)
    
    def post(request):
        try:
            user = request.user
            if user.type == 2:
                product = request.POST.get('product')
                quantity = int(request.POST.get('quantity'))
                a = Card.objects.create(product=product,quantity=quantity,user=user)
                ser = CardSerializer(a)
                return Response(ser.data)
        except Exception as err:
            data = {
                'error': f'{err}'
            }
            return Response(data)

class Purchase(APIView):
    def post(request, pk):
        user = request.user
        if user.type == 2:
            card = Card.objects.get(user_id=pk)
            pr = card.product.id
            product = Product.objects.filter(id=pr)
            if product.quantity == 0:
                product.soldout = True
                product.save()
            product.quantity - card.quantity
            product.save()
            return Response()
