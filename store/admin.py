from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'price', 'stock')
    list_filter = ('vendor',)
    search_fields = ('name', 'vendor__username')

admin.site.register(Product, ProductAdmin)
