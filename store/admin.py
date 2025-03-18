from django.contrib import admin
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']
    list_editable = ['image']
    prepopulated_fields = {'slug': ('title',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'price', 'stock')
    list_filter = ('vendor',)
    search_fields = ('name', 'vendor__username')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
