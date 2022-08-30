from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    type = models.IntegerField(choices=(
        (1, 'admin'),
        (2, 'client'),
    ), default=2)
    phone = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Info(models.Model):
    logo = models.ImageField(upload_to='logo/')
    ins = models.URLField()
    f = models.URLField()
    insta = models.URLField()
    twitter = models.URLField()

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Production(models.Model):
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='product/')
    image2 = models.ImageField(upload_to='product/')
    image3 = models.ImageField(upload_to='product/', null=True, blank=True)
    image4 = models.ImageField(upload_to='product/', null=True, blank=True)
    image5 = models.ImageField(upload_to='product/', null=True, blank=True)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(validators=[MaxValueValidator(1000000),MinValueValidator(0)])
    sku = models.IntegerField()
    description = models.TextField()
    weight = models.FloatField()
    dimentions = models.CharField(max_length=25)
    colors = models.CharField(max_length=255)
    material = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    soldout = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0,validators=[MaxValueValidator(1000000), MinValueValidator(0)])
    production = models.ForeignKey(Production, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=15)
    reviews = models.IntegerField(default=0, null=True, blank=True)
    discount_price = models.IntegerField(default=0,validators=[MaxValueValidator(100),MinValueValidator(0)])
    date =  models.DateField(auto_now_add=True)
    rating = models.FloatField(default=1,validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self):
        return self.production.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=255)
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)
    rating = models.FloatField(default=1,validators=[MaxValueValidator(5), MinValueValidator(1)])

class Contact(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

class Blog(models.Model):
    theme = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='product/')
    image2 = models.ImageField(upload_to='product/')
    image3 = models.ImageField(upload_to='product/', null=True, blank=True)
    text = models.TextField()
    text2 =  models.TextField()
    text3 =  models.TextField(null=True, blank=True)
    text4 =  models.TextField(null=True, blank=True)
    category = models.ManyToManyField(Category)

class Reply(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=255)
    unauthorized = models.GenericIPAddressField(blank=True,null=True)
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)

class About(models.Model):
    theme = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)
    text2 = models.TextField(null=True, blank=True)
    text3 = models.TextField(null=True, blank=True)
    text4 = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='about/')
    image2 = models.ImageField(upload_to='about/')
    image3 = models.ImageField(upload_to='about/', blank=True, null=True)

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    unauthorized = models.GenericIPAddressField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)

class Purchase(models.Model):
    card = models.ForeignKey("Card", on_delete=models.CASCADE)
    summa = models.DecimalField(decimal_places=2,max_digits=15)
    cash = models.DecimalField(decimal_places=2,max_digits=15, null=True, blank=True)

class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Newsletter(models.Model):
    email = models.EmailField()

class BilingAddress(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    companyname = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    phone = models.IntegerField()
    email = models.EmailField()

class Checkout(models.Model):
    couponcode = models.CharField(max_length=255)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    companyname = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    phone = models.IntegerField()
    email = models.EmailField()
    shiptootherplace = models.CharField(max_length=255,null=True,blank=True)
    ordernotes = models.TextField()

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity =  models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    unauthorized = models.GenericIPAddressField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)