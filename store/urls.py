from django.urls import path
from .views import HomePageView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView


urlpatterns = [
    #path('',)
    path('',HomePageView.as_view(), name='home'),
    path('product/<int:pk>/',ProductDetailView.as_view(),name='product_detail' ),
    path('product/new/', ProductCreateView.as_view(), name='product_new'),
    path('product/<int:pk>/edit', ProductUpdateView.as_view(), name ='product_edit'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]