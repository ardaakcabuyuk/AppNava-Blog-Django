from django.shortcuts import render
from .models import Blog

def homepage(request):
    return render(request, 'blogs/posts.html')

def add_blog(request):
    if request.method == 'POST':
        if request.POST.get('title') and request.POST.get('abstract') and request.POST.get('body'):
            blog=Blog()
            blog.title= request.POST.get('title')
            blog.abstract= request.POST.get('abstract')
            blog.body= request.POST.get('body')
            blog.save()

            return render(request, 'blogs/add_blog.html')

    else:
            return render(request,'blogs/add_blog.html')
