from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from .models import Blog
from datetime import datetime

def homepage(request):
    return render(request, 'blogs/posts.html') #posts.html extends homepage.html

def add_blog(request):
    #if user clicks 'add' button
    if request.method == 'POST':

        #title, abstract and body are required fields
        if request.POST.get('title') and request.POST.get('abstract') and request.POST.get('body'):

            #create new blog
            blog=Blog()

            #get user inputs from fields
            blog.title= request.POST.get('title')
            blog.abstract= request.POST.get('abstract')
            blog.body= request.POST.get('body')

            #unless specified, date fields are set to default (publish date -> now(), removal_date -> None)
            if request.POST.get('publish_date'):
                blog.publish_date = request.POST.get('publish_date')
            if request.POST.get('removal_date'):
                blog.removal_date = request.POST.get('removal_date')

            #save the post
            blog.save()

            #go to homepage
            return HttpResponseRedirect('/')

    else:
            return render(request,'blogs/add_blog.html')

def delete_blog(request, pk=None):
    #get the id of the selected post
    blog = Blog.objects.get(id=pk)

    #set the removal date to click time
    blog.removal_date = datetime.now()

    #save the state
    blog.save()

    #redirect to the same page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def edit_blog(request, pk=None):
    #get the id of the selected post
    blog = Blog.objects.get(id=pk)

    #create nested dictionaries.they will be passed to edit_blog.html in order to get prefilled fields
    dic = ({"title":blog.title, "abstract":blog.abstract, "body":blog.body, "publish_date":blog.publish_date, "removal_date":blog.removal_date})
    dict2 = {"dict1":dic} #this step is required because we will simply pass dict2 to edit_blog.html and call dict1.title, for example

    #if user clicks 'update' button
    if request.method == 'POST':

        #title, abstract and body are required fields
        if request.POST.get('title') or request.POST.get('abstract') or request.POST.get('body'):

            #get user inputs from fields
            blog.title= request.POST.get('title')
            blog.abstract= request.POST.get('abstract')
            blog.body= request.POST.get('body')

            #unless specified, date fields will stay same
            if request.POST.get('publish_date'):
                blog.publish_date = request.POST.get('publish_date')
            if request.POST.get('removal_date'):
                blog.removal_date = request.POST.get('removal_date')

            #save the post
            blog.save()

            #return to homepage
            return HttpResponseRedirect('/')

    else:
        #to get the prefilled form before user clicks updates the post
        return render(request, 'blogs/edit_blog.html', dict2)

def search(request):
    #get all objects (order by -publish_date which is the same as homepage)
    qs = Blog.objects.all().order_by('-publish_date')

    #get user queries
    title_query = request.GET.get("title")
    abstract_query = request.GET.get("abstract")
    publish_date_query = request.GET.get("publish_date")
    removal_date_query = request.GET.get("removal_date")

    #after clicking search button, we save the queries in a dictionary to keep them in their fields
    ql = {"title":title_query, "abstract":abstract_query, "publish_date":publish_date_query, "removal_date": removal_date_query}

    #filter the posts according to the queries
    if title_query != '' and title_query is not None:
        qs = qs.filter(title__icontains=title_query)

    if abstract_query != '' and abstract_query is not None:
        qs = qs.filter(abstract__icontains=abstract_query)

    if publish_date_query != '' and publish_date_query is not None:
        qs = qs.filter(publish_date__icontains=publish_date_query)

    if removal_date_query != '' and removal_date_query is not None:
        qs = qs.filter(removal_date__icontains=removal_date_query)

    #this dictionary will be passed to posts.html (and homepage.html since posts.html extends it)
    context = {
        "object_list": qs,
        "query_list": ql
    }
    
    return render(request, "blogs/posts.html", context)
