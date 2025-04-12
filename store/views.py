from django.shortcuts import render , get_object_or_404 , redirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product , Review
from .forms import ReviewForm


class HomePageView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = "all_products_list"

class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"

class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"

class VendorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return self.request.user.groups.filter(name='Vendor').exists()

class ProductCreateView(LoginRequiredMixin, VendorRequiredMixin, CreateView):
    model = Product
    template_name = 'product_new.html'
    fields = ['name','description', 'image', 'price', 'stock']

    def form_valid(self, form):
        form.instance.vendor = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = 'product_edit.html'
    fields = ['price', 'stock']

    def test_func(self):
        product = self.get_object()
        return self.request.user.is_superuser or product.vendor == self.request.user

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        product = self.get_object()
        return self.request.user.is_superuser or product.vendor == self.request.user

class SearchResultsListView(ListView):
    model = Product
    template_name = "search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return Product.objects.none()


def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('product_detail', product_id=product_id)
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'form': form, 'product': product})