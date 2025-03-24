from django.contrib import admin
from blog import models as blog_models

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'views', 'date']
    search_fields = ['title', 'author__username', 'category__name']
    list_filter = ['status', 'is_featured', 'category', 'date']
    prepopulated_fields = {'slug': ('title',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'blog', 'approved', 'date']
    search_fields = ['full_name', 'email', 'blog__title']
    list_filter = ['approved', 'date']

admin.site.register(blog_models.Category, CategoryAdmin)
admin.site.register(blog_models.Blog, BlogAdmin)
admin.site.register(blog_models.Comment, CommentAdmin)