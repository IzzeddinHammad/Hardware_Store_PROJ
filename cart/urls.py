from django.urls import path
from . import views
from .views import CartItem


app_name='cart'
urlpatterns = [
    path('add/<int:pk>/', views.add_cart, name='add_cart'),
    path('', views.cart_detail, name='cart_detail'),
    path('remove/<uuid:product_id>/',views.cart_remove,name='cart_remove'),
    path('full_remove/<uuid:product_id>/',views.full_remove, name='full_remove'),
    path('<uuid:pk>/', views.CartItem, name='cart')
]