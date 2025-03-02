from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<uuid:product_id>/', views.add_cart, name='add_cart'),
    path('remove/<uuid:product_id>/', views.cart_remove, name='cart_remove'),
    path('full_remove/<uuid:product_id>/', views.full_remove, name='full_remove'),
    path('', views.cart_detail, name='cart_detail'),
    path('empty/', views.empty_cart, name='empty_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('new_order/', views.create_order, name='new_order'),
]
