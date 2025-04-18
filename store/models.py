import uuid
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.contrib.auth import get_user_model

class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images", default="category.jpg", null=True, blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

    def products(self):
        return Product.objects.filter(category=self)

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    creator = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='created_products',
        null=False
    )

    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')

    category = models.ForeignKey(Category , on_delete=models.SET_NULL , null=True , blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[str(self.id)])



class Rating(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stars = models.PositiveIntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    rating = models.OneToOneField(Rating, on_delete=models.CASCADE, related_name='review')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)