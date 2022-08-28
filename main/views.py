from rest_framework.decorators import APIView
from rest_framework.response import Response
from .models import *
from .serializer import *
from ipware import get_client_ip

class InfoGET(APIView):
    def get(self, request):
        info = Info.objects.last()
        ser = InfoSerializer(info)
        return Response(ser.data)

class SliderGET(APIView):
    def get(self, request):
        product = Product.objects.all().order_by('rating')[:5]
        ser = ProductSerializer(product, many=True)
        return Response(ser.data)

class Latest(APIView):
    def get(self, request):
        product = Product.objects.all().order_by('-id')[:6]
        ser = ProductSerializer(product, many=True)
        return Response(ser.data)

class NewletterPOST(APIView):
    def post(self, request):
        email = request.data['email']
        news = Newsletter.objects.create(email=email)
        ser = NewsletterSerializer(news)
        return Response(ser.data)

class Search(APIView):
    def get(self, request):
        nam = request.data['name']
        found = Production.objects.filter(name__icontains=nam)
        ser = ProductionSerializer(found, many=True)
        return Response(ser.data)

class Filter(APIView):
    def post(self, request):
        firstprice = int(request.data['firstprice'])
        secondprice = int(request.data['secondprice'])
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
        Data = {
                "products": []
            }
        for i in product:
            if i.quantity <= 0:
                i.soldout = True
                i.save()
                Data['products'].append(ProductSerializer(i).data)
            else:
                i.soldout = False
                i.save()
                Data['products'].append(ProductSerializer(i).data)
        return Response(Data)
    
    def post(self, request, pk):
        a = Production.objects.get(id=pk)
        quantity = int(request.data['quantity'])
        if quantity > a.quantity:
            return Response('error quantity')
        else:
            b = a.quantity - quantity
            a.quantity = b
            print(a.quantity)
            a.save()
            myquantity = quantity
        price = float(request.data['price'])
        discount_price = int(request.data['discount'])
        if discount_price > 0:
            myprice = price - (price * discount_price / 100)
            b = Product.objects.create(product_id=a.id, price=myprice,quantity=myquantity, discount_price=discount_price)
            ser = ProductSerializer(b)
            return Response(ser.data)
        else:
            Product.objects.create(product_id=a.id, price=price,quantity=myquantity)
            return Response(ser.data)

class ProductionView(APIView):
    def get(self, request):
        production = Production.objects.all()
        ser = ProductionSerializer(production, many=True)
        return Response(ser.data)

    def post(self, request):
        try:
            user = request.user
            if user.type == 1:
                category = int(request.data['category'])
                image = request.FILES['image']
                image2 = request.FILES['image2']
                image3 = request.FILES['image3']
                image4 = request.FILES['image4']
                image5 = request.FILES['image5']
                name = request.data['name']
                quantity = int(request.data['quantity'])
                sku = request.data['sku']
                description = request.data['description']
                weight = request.data['weight']
                dimentions = request.data['dimentions']
                material = request.data['material']
                colors = request.data['colors']
                price = request.data['price']
                discount_price = request.data['discount_price']
                z = Production.objects.filter(name=name, category=category, sku=sku, weight=weight,
                dimentions=dimentions,colors=colors,material=material)
                if quantity <= 0:
                    return Response('error')
                else:
                    productions = Production.objects.all()
                    for qwe in productions:
                        for ids in qwe.category.all():
                            if ids.id == category:
                                if len(z)==0:
                                    a = Production.objects.create(
                                    image=image, image2=image2,image3=image3,
                                    image4=image4, image5=image5,name=name,quantity=quantity,sku=sku,description=description,
                                    weight=weight,dimentions=dimentions,material=material, colors=colors)
                                    a.category.set(category)
                                    a.save()
                                    prod = Product.objects.create(production_id=a.id, price=price, discount_price=discount_price)
                                    b = prod.quantity + quantity
                                    prod.quantity = b
                                    prod.save()
                                    ser = ProductionSerializer(a)
                                    return Response(ser.data)
                                else:
                                    for i in z:
                                        if i.name == name:
                                            prod = Product.objects.get(production_id=i.id)
                                            b = prod.quantity + quantity
                                            prod.quantity = b
                                            prod.save()
                                            ser = ProductSerializer(prod)
                                            return Response(ser.data)
                                        else:
                                            a = Production.objects.create(
                                            image=image, image2=image2,image3=image3,
                                            image4=image4, image5=image5,name=name,quantity=quantity,sku=sku,description=description,
                                            weight=weight,dimentions=dimentions,material=material, colors=colors)
                                            a.category.set(category)
                                            a.save()
                                            prod = Product.objects.create(production_id=a.id, price=price, discount_price=discount_price)
                                            b = prod.quantity + quantity
                                            prod.quantity = b
                                            prod.save()
                                            ser = ProductionSerializer(a)
                                            return Response(ser.data)
                            else:
                                return Response('errorqweqwe')
            else:
                return Response("You can't do this action!")
        except Exception as er:
            data = {
                'error': f"{er}"
            }
            return Response(data)

class CardView(APIView):
    def get(self, request):
        try:
            user = request.user
            if not user.is_anonymous:
                if user.type == 2:
                    card = Card.objects.filter(user_id=user)
                    data = ["Card items"]
                    for i in card:
                        Data = {
                            "name": "",
                            "price": 0,
                            "quantity": 0,
                            "discount": 0,
                            "total price": 0,
                        }
                        Data['price'] = i.product.price
                        Data['discount'] = i.product.discount_price
                        g = i.product.price * i.product.discount_price/100
                        Data['total price'] += i.quantity * (i.product.price - g)
                        Data['name'] = i.product.production.name
                        Data['quantity'] = i.quantity
                        data.append(Data)
            else:
                client_ip = get_client_ip(request)
                card = Card.objects.filter(unauthorized=client_ip)
                data = ["Card items"]
                for i in card:
                    Data = {
                        "name": "",
                        "price": 0,
                        "price with discount": 0,
                        "discount": 0,
                        "quantity": 0,
                        "total price": 0,
                    }
                    Data['price'] = i.product.price
                    Data['discount'] = i.product.discount_price
                    g = i.product.price * i.product.discount_price/100
                    Data['price with discount'] = i.product.price - g
                    Data['total price'] += i.quantity * (i.product.price - g)
                    Data['name'] = i.product.production.name
                    Data['quantity'] = i.quantity
                    data.append(Data)
            return Response(data)
        except Exception as er:
            data = {
                'error':f"{er}"
            }
            return Response(data)
    
    def post(self, request):
        try:
            user = request.user
            if not user.is_anonymous:
                product = request.data['product']
                quantity = int(request.data['quantity'])
                pro = Product.objects.get(id=product)
                user = request.user
                if user.type == 2:
                    if pro.quantity < quantity:
                        return Response('quantity value error')
                    else:
                        a = Card.objects.create(product_id=product,quantity=quantity, user=user, unauthorized=None)
                        ser = CardSerializer(a)
                        return Response(ser.data)
                else:
                    return Response("you can't")
            else:
                product = request.data['product']
                quantity = int(request.data['quantity'])
                pro = Product.objects.get(id=product)
                client_ip = get_client_ip(request)
                Data = {
                    "card": ()
                }
                if client_ip is None:
                    return Response("You can't do this action!!!")
                    # Unable to get the client's IP address
                else:
                    if pro.quantity < quantity:
                        return Response('quantity value error')
                    else:
                        a = Card.objects.create(product_id=product,quantity=quantity,unauthorized=client_ip)
                        ser = CardSerializer(a)
                        Data['card'] = ser.data
                    # We got the client's IP address
                return Response(Data)
        except Exception as err:
            data = {
                'error': f'{err}'
            }
            return Response(data)

class PurchaseView(APIView):
    def get(self, request):
        try:
            user = request.user
            client_ip = get_client_ip(request)
            Data = {
                "products": [],
                "total": 0
            }
            if not user.is_anonymous:
                if user.type == 2:
                    purchases = Purchase.objects.filter(card_user_id=user)
                    for i in purchases:
                        g = i.card.product.price * i.card.product.discount_price/100
                        Data['total'] += i.card.quantity * (i.card.product.price - g)
                        ser = ProductSerializer(i.card.product)
                        Data['products'].append(ser.data)
            else:
                purchases = Purchase.objects.filter(card__unauthorized=client_ip)
                for i in purchases:
                    g = i.card.product.price * i.card.product.discount_price/100
                    Data['total'] += i.card.quantity * (i.card.product.price - g)
                    ser = ProductSerializer(i.card.product)
                    Data['products'].append(ser.data)
            return Response(Data)
        except Exception as er:
            data = {
                'error': f'{er}'
            }
            return Response(data)

    def post(self, request):
        try:
            user = request.user
            client_ip = get_client_ip(request)
            Data = {
                "products": [],
                "total": 0
            }
            if not user.is_anonymous:
                if user.type == 2:
                    mycard = Card.objects.filter(user_id=user)
                    for i in mycard:
                        g = i.product.price * i.product.discount_price/100
                        Data['total'] += i.quantity * (i.product.price - g)
                        ser = ProductSerializer(i.product)
                        Data['products'].append(ser.data)
                    card = Card.objects.get(user_id=user)
                    pr = card.product.id
                    summa = int(request.data['summa'])
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
                            remain = summa - summ
                            purchase = Purchase.objects.create(card_id=card.id, summa=summ, cash=remain)
                            card.delete()

                            ser = PurchaseSerializer(purchase)
                            return Response(ser.data)
            else:
                mycard = Card.objects.filter(unauthorized=client_ip)
                for i in mycard:
                    Data['total'] += i.quantity * i.product.price
                    ser = ProductSerializer(i.product)
                    Data['products'].append(ser.data)
                card = Card.objects.get(unauthorized=client_ip)
                pr = card.product.id
                summa = int(request.data['summa'])
                product = Product.objects.get(id=pr)
                g = card.product.price * card.product.discount_price/100
                summ =  (card.product.price - g) * card.quantity
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
                        remain = summa - summ
                        purchase = Purchase.objects.create(card_id=card.id, summa=summ, cash=remain)
                        card.delete()
                        ser = PurchaseSerializer(purchase)
                        return Response(ser.data)
        except Exception as er:
            data = {
                'error': f"{er}"
            }
            return Response(data)
## OK
class Reviewing(APIView):
    def get(self, request, pk):
        product = Product.objects.all()
        review = Review.objects.filter(product_id=pk)
        data = [{'rating':0}]
        a = 0
        for i in product:
            for r in review:
                Data = {
                    'username': "",
                    'product': '',
                    'rating': '',
                    'comment': "",
                    'date': "",
                }
                a += r.rating
                i.rating = a/len(review)
                i.save()
                data[0]=f"rating: {i.rating}"
                Data['product']=i.production.name
                Data['username']=r.username
                Data['date']=r.date
                Data['comment']=r.comment
                Data['rating']=r.rating
                data.append(Data)
        return Response(data)

    def post(self, request,pk):
        try:
            user = request.user
            client_ip = get_client_ip(request)
            if not user.is_anonymous:
                comment = request.data['comment']
                rating = request.data['rating']
                review = Review.objects.create(user_id=user.id, username=user.username, product_id=pk,comment=comment,rating=rating)
                ser = ReviewSerializer(review)
                return Response(ser.data)
            else:
                if client_ip is None:
                    return Response("You can't do this action!!!")
                    # Unable to get the client's IP address
                else:
                    username = request.data['username']
                    comment = request.data['comment']
                    rating = request.data['rating']
                    review = Review.objects.create(username=username, product_id=pk,comment=comment,rating=rating)
                    ser = ReviewSerializer(review)
                    return Response(ser.data)
        except Exception as er:
            data = {
                'error': f"{er}"
            }
            return Response(data)
###


class Contacting(APIView):
    def get(request, self):
        contact = Contact.objects.last()
        ser = ContactSerializer(contact)
        return Response(ser.data)

class Bloging(APIView):
    def get(request, self):
        blog = Blog.objects.all()
        ser = BlogSerializer(blog, many=True)
        return Response(ser.data)

class BlogingPK(APIView):
    def get(request, self, pk):
        blog = Blog.objects.get(id=pk)
        ser = BlogSerializer(blog)
        return Response(ser.data)

class Abouting(APIView):
    def get(request, self):
        about = About.objects.all()
        ser = AboutSerializer(about, many=True)
        return Response(ser.data)

class Replies(APIView):
    def get(request, self, pk):
        reply = Reply.objects.get(blog_id=pk)
        ser = ReplySerializer(reply)
        return Response(ser.data)

    def post(request,self,pk):
        try:
            user = request.user
            blog = Blog.objects.get(id=pk)
            comment = request.data['comment']
            reply = Reply.objects.create(blog_id=blog,user=user,comment=comment)
            ser = ReplySerializer(reply)
            return Response(ser.data)
        except Exception as er:
            data = {
                'error': f"{er}"
            }
            return Response(data)