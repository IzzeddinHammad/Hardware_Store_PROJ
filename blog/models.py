from django.db import models
from accounts import models as accounts_models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.utils import timezone

STATUS_CHOICES = [
    ('Draft', 'Draft'),
    ('Published', 'Published'),
]

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Blog(models.Model):
    image = models.ImageField(upload_to='blog_images', blank=True, null=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=350, unique=True, blank=True)
    author = models.ForeignKey(accounts_models.User, on_delete=models.CASCADE)
    content = CKEditor5Field(config_name='extends', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Published")
    likes = models.ManyToManyField(accounts_models.User, blank=True, related_name="likes")
    views = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.all().count()

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.full_name} on {self.blog.title}"
