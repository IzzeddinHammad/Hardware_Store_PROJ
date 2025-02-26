from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
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