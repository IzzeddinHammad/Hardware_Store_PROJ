from django.urls import path
from .views import (
    HomePageView, ProductDetailView, ProductCreateView, 
    ProductUpdateView, ProductDeleteView, SearchResultsListView, ProductListView
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/new/', ProductCreateView.as_view(), name='product_new'),
    path('products/<uuid:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<uuid:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('products/<uuid:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
]
