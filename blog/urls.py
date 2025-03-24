from django.urls import path
from blog import views

app_name = "blog"

urlpatterns = [
    path("", views.blog_list, name="blog_list"),
    path("blog_detail/<slug>/", views.blog_detail, name="blog_detail"),
    path("create_comment/<slug>/", views.create_comment, name="create_comment"),
    path("like_blog/", views.like_blog, name="like_blog"),
    

]