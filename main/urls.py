from django.urls import path
from .views import *

urlpatterns = [
    path('product/', ProductView.as_view()),
    path('info/', InfoGET.as_view()),
    path('slider/', SliderGET.as_view()),
    path('latest/', Latest.as_view()),
    path('review/<int:pk>/', Reviewing.as_view()),

    path('product/<int:pk>/', ProductView.as_view()),
    path('productget/<int:pk>/', ProductPk.as_view()),
    path('production/', ProductionView.as_view()),
    path('purchase/', PurchaseView.as_view()),
    path('cardview/', CardView.as_view()),

    path('contact/', Contacting.as_view()),
    path('blog/', Bloging.as_view()),
    path('blog/<int:pk>', BlogingPK.as_view()),
    path('newletter/', NewletterPOST.as_view()),

    path('search/', Search.as_view()),
    path('filter/', Filter.as_view()),
    path('about/', Abouting.as_view()),
    path('reply/<int:pk>', Replies.as_view()),

    path('instock/', Instock.as_view()),
    path('onsale/', Onsale.as_view()),
]