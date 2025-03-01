from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .models import Product
# Create your views here.

from django.urls import reverse_lazy

class HomePageView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = "all_products_list"

class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"

class ProductCreateView(CreateView):
    model = Product
    template_name = 'product_new.html'
    fields = ['name', 'image', 'price', 'stock']

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product_edit.html'
    fields= ['price', 'stock']
class ProductDeleteView(DeleteView):
    model = Product
    template_name='product_delete.html'
    success_url = reverse_lazy('home')

class SearchResultsListView(ListView):
    model = Product
    template_name = "search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Product.objects.filter(
                Q(name__icontains=query) |
                Q(price__icontains=query)
            )
        return Product.objects.none()