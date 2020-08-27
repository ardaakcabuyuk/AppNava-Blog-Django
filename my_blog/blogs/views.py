from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
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

def delete_blog(request, pk=None):
    blog = Blog.objects.get(id=pk)
    blog.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def edit_blog(request, pk=None):
    blog = Blog.objects.get(id=pk)
    dic = ({"title":blog.title, "abstract":blog.abstract, "body":blog.body})
    dict2 = {"dict1":dic}

    if request.method == 'POST':
        if request.POST.get('title') or request.POST.get('abstract') or request.POST.get('body'):
            blog.title= request.POST.get('title')
            blog.abstract= request.POST.get('abstract')
            blog.body= request.POST.get('body')
            blog.save()
            dic = ({"title":blog.title, "abstract":blog.abstract, "body":blog.body})
            dict2 = {"dict1":dic}
            return render(request, 'blogs/edit_blog.html', dict2)

    else:
        return render(request, 'blogs/edit_blog.html', dict2)
