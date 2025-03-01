from django.urls import path
from .views import HomePageView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, SearchResultsListView

app_name = 'store'  

urlpatterns = [
    path('',HomePageView.as_view(), name='home'),
    path('product/<uuid:id>/',ProductDetailView.as_view(),name='product_detail' ),
    path('product/new/', ProductCreateView.as_view(), name='product_new'),
    path('product/<uuid:id>/edit', ProductUpdateView.as_view(), name ='product_edit'),
    path('product/<uuid:id>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
]