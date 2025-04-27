from django.urls import path
from . import views

url = [
    path('trending', views.trending_product, name= 'trending_product'),
]

