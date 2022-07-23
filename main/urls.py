from django.urls import path
from .views import *

urlpatterns = [
    path('product/<int:pk>', ProductView.as_view()),
    path('production/', ProductionView.as_view()),
    path('purchase/', PurchaseView.as_view()),
    path('card/', CardView.as_view()),
]