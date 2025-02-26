from django.views.generic import TemplateView, DetailView, ListView
from .models import Product
# Create your views here.

class HomePageView(ListView):
    model = Product 
    template_name = 'home.html'
    context_object_name = "all_products_list"

class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"