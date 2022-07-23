import sre_compile
from urllib import request
from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .models import *
from .serializer import *
from django.core.exceptions import ObjectDoesNotExist
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
    def post(self, request):
        try:
            category = request.POST.get('category')
            image = request.FILES['image']
            image2 = request.FILES['image2']
            image3 = request.FILES['image3']
            image4 = request.FILES['image4']
            image5 = request.FILES['image5']
            name = request.POST.get('name')
            quantity = int(request.POST.get('quantity'))
            sku = request.POST.get('sku')
            description = request.POST.get('description')
            weight = request.POST.get('weight')
            dimentions = request.POST.get('dimentions')
            material = request.POST.get('material')
            colors = request.POST.get('colors')
            price = request.POST.get('price')
            discount_price = request.POST.get('discount_price')
            ##
            
            z = Production.objects.all()
            for i in z:
                if i.name == name:
                    prod = Product.objects.get(production_id=i.id)
                    b = prod.quantity + quantity
                    prod.quantity = b
                    prod.save()
                else:
                    a = Production.objects.create(
                    image=image, image2=image2,image3=image3,
                    image4=image4, image5=image5,name=name,quantity=quantity,sku=sku,description=description,
                    weight=weight,dimentions=dimentions,material=material, colors=colors)
                    a.category.set(category)
                    a.save()
                    prod = Product.objects.create(production_id=i.id, price=price, discount_price=discount_price)
                    b = prod.quantity + quantity
                    prod.quantity = b
                    prod.save()
            ser = ProductionSerializer(a)
            return Response(ser.data)
        except Exception as er:
            data = {
                'error': f"{er}"
            }
            return Response(data)

class CardView(APIView):
    def get(self, request, pk):
        card = Card.objects.get(user_id=pk)
        ser = CardSerializer(card)
        return Response(ser.data)
    
    def post(self, request):
        try:
            user = request.user
            if user.type == 2:
                product = request.POST.get('product')
                quantity = int(request.POST.get('quantity'))
                pro = Product.objects.get(id=product)
                if pro.quantity < quantity:
                    return Response('quantity value error')
                else:
                    a = Card.objects.create(product_id=product,quantity=quantity,user=user)
                    ser = CardSerializer(a)
                    return Response(ser.data)
        except Exception as err:
            data = {
                'error': f'{err}'
            }
            return Response(data)

class PurchaseView(APIView):
    def post(self, request):
        try:
            user = request.user
            if user.type == 2:
                card = Card.objects.get(user_id=user)
                pr = card.product.id
                summa = int(request.POST.get('summa'))
                product = Product.objects.get(id=pr)
                summ =  card.product.price * card.quantity
                if summa < summ:
                    return Response(f"you have to pay:{summ}")
                else:
                    if product.quantity == 0:
                        product.soldout = True
                        product.save()
                        return Response("it's been already sold")
                    elif product.quantity < card.quantity:
                        return Response("We don't have so many items -> 'quantity'")
                    else:
                        a = product.quantity - card.quantity
                        product.quantity = a
                        product.save()
                        purchase = Purchase.objects.create(card_id=card.id, summa=summ)
                        ser = PurchaseSerializer(purchase)
                        return Response(ser.data)
        except Exception as er:
            data = {
                'error': f"{er}"
            }
            return Response(data)