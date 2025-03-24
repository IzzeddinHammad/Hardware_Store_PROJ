from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from blog import models as blog_models
from plugin.paginate_queryset import paginate_queryset
from django.contrib import messages

def blog_list(request):
    blogs_list = blog_models.Blog.objects.all().order_by('-date') 
    blogs = paginate_queryset(request, blogs_list, 10)

    context = {
        'blogs': blogs,
        'blogs_list': blogs_list,
    }
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, slug):
    blog = get_object_or_404(blog_models.Blog, slug=slug) 
    comments = blog.comments.filter(approved=True)  

    liked = False
    if blog.likes.filter(id=request.user.id).exists():
        liked = True

    context = {
        'blog': blog,
        'comments': comments,
        'liked': liked,
        'total_likes': blog.total_likes(),
    }
    return render(request, 'blog/blog_detail.html', context)

def create_comment(request, slug):
    blog = get_object_or_404(blog_models.Blog, slug=slug)
    if request.method == 'POST':
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        content = request.POST.get("content")

        blog_models.Comment.objects.create(
            blog=blog,
            full_name=full_name,
            email=email,
            content=content,
        )

    messages.success(request, "Comment created, awaiting moderation!")
    return redirect('blog:blog_detail', slug=blog.slug)

def like_blog(request):
    blog = get_object_or_404(blog_models.Blog, id=request.POST.get('blog_id'))
    if blog.likes.filter(id=request.user.id).exists():
        blog.likes.remove(request.user)
        liked = False
    else:
        blog.likes.add(request.user)
        liked = True
    
    context = {
        'total_likes': blog.total_likes(),
        'liked': liked,
    }

    if request.is_ajax():
        return JsonResponse(context)

    return redirect('blog_detail', slug=blog.slug)