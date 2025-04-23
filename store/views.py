from django.shortcuts import render , get_object_or_404 , redirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product , Rating , Category
from django.contrib import messages
from .forms import RatingForm , ReviewForm , ProductForm

class HomePageView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = "all_products_list"

    def get_queryset(self):

        queryset = super().get_queryset()
        category_slug = self.request.GET.get('category')

        if category_slug:
            queryset = queryset.filter(category__slug = category_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


def my_products_view(request):
    products = Product.objects.filter(creator=request.user)
    return render(request, 'my_products.html', {'products': products})

class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.GET.get('category')

        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=self.category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        if hasattr(self, 'category'):
            context['current_category'] = self.category

        return context

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
    fields = ['name','description', 'image', 'price', 'stock', 'category']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.vendor = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = 'product_edit.html'
    fields = ['price', 'stock']
    success_url = reverse_lazy('store:product_list')

    def test_func(self):
        product = self.get_object()
        return self.request.user.is_superuser or product.vendor == self.request.user



class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('store:home')

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



def rate_item(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        review_form = ReviewForm(request.POST)

        if rating_form.is_valid() and review_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.item = product
            rating.user = request.user
            rating.save()

            review = review_form.save(commit=False)
            review.rating = rating
            review.save()

            messages.success(request, "Your rating and review have been saved!")
            return redirect('store:product_detail', pk=product_id)
    else:
        rating_form = RatingForm()
        review_form = ReviewForm()

    return render(request, 'product_detail.html', {
        'product': product,
        'rating_form': rating_form,
        'review_form': review_form
    })



def remove_rating(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id, user=request.user)
    product_id = rating.item.id
    rating.delete()
    messages.success(request, "Rating deleted successfully")
    return redirect('store:product_detail', pk=product_id)



def edit_product(request,product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST , instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail')

    else:
        form = ProductForm(instance=product)

    return render(request , 'product_edit.html' , {'form':form})




