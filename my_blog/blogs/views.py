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

def search(request):
    qs = Blog.objects.all()
    title_query = request.GET.get("title")
    abstract_query = request.GET.get("abstract")
    publish_date_query = request.GET.get("publish_date")
    removal_date_query = request.GET.get("removal_date")

    if title_query != '' and title_query is not None:
        qs = qs.filter(title__icontains=title_query)

    elif abstract_query != '' and abstract_query is not None:
        qs = qs.filter(abstract__icontains=abstract_query)

    elif publish_date_query != '' and publish_date_query is not None:
        qs = qs.filter(publish_date__icontains=publish_date_query)

    elif removal_date_query != '' and removal_date_query is not None:
        qs = qs.filter(removal_date__icontains=removal_date_query)


    context = {
        "queryset": qs
    }

    return render(request, "blogs/results.html", context)
