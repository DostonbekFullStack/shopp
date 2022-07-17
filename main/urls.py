from django.urls import path
from .views import *
urlpatterns = [
    path('productpost/<int:pk>', ProductView.as_view())
]