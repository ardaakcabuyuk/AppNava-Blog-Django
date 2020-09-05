from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from .models import Blog
from datetime import datetime, timedelta

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
            if request.POST.get('publish_date') and request.POST.get('removal_date') and request.POST.get('publish_date') > request.POST.get('removal_date'):
                pass
            else:
                if request.POST.get('publish_date'):
                    blog.publish_date = request.POST.get('publish_date')
                if request.POST.get('removal_date'):
                    blog.removal_date = request.POST.get('removal_date')

            #save the post
            blog.save()

            #go to homepage
            return HttpResponseRedirect('/')

    else:
            return HttpResponseRedirect('/')

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

    #get selected post
    blog = Blog.objects.get(id=pk)


    #if user clicks 'update' button
    if request.method == 'POST':

        #title, abstract and body are required fields
        if request.POST.get('title') or request.POST.get('abstract') or request.POST.get('body'):

            #get user inputs from fields
            blog.title= request.POST.get('title')
            blog.abstract= request.POST.get('abstract')
            blog.body= request.POST.get('body')

            #unless specified, date fields will stay same
            if request.POST.get('publish_date') and request.POST.get('removal_date') and request.POST.get('publish_date') > request.POST.get('removal_date'):
                pass
            else:
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
        return HttpResponseRedirect('/')

def search(request):
    #get all objects (order by -publish_date which is the same as homepage)
    qs = Blog.objects.all().order_by('-publish_date')

    #get user queries
    title_query = request.GET.get("title")
    abstract_query = request.GET.get("abstract")
    publish_date_min_query = request.GET.get("publish_date_min")
    publish_date_max_query = request.GET.get("publish_date_max")
    removal_date_min_query = request.GET.get("removal_date_min")
    removal_date_max_query = request.GET.get("removal_date_max")

    #filter the posts according to the queries
    if title_query != '' and title_query is not None:
        qs = qs.filter(title__icontains=title_query)

    if abstract_query != '' and abstract_query is not None:
        qs = qs.filter(abstract__icontains=abstract_query)

    if publish_date_min_query != '' and publish_date_min_query is not None and publish_date_max_query == '':
        qs = qs.filter(publish_date__range=[publish_date_min_query, "9999-12-31"])

    #added 1 day to the upper end of date range, because upper end is exclusive
    if publish_date_max_query != '' and publish_date_max_query is not None and publish_date_min_query == '':
        qs = qs.filter(publish_date__range=["1000-01-01", datetime.strptime(publish_date_max_query, "%Y-%m-%d").date() + timedelta(days=1)])


    if publish_date_min_query != '' and publish_date_max_query != '' and publish_date_min_query < publish_date_max_query:
        qs = qs.filter(publish_date__range=[publish_date_min_query, datetime.strptime(publish_date_max_query, "%Y-%m-%d").date() + timedelta(days=1)])

    else:
        publish_date_min_query = ''
        publish_date_max_query = ''

    if removal_date_min_query != '' and removal_date_min_query is not None and removal_date_max_query == '':
        qs = qs.filter(removal_date__range=[removal_date_min_query, "9999-12-31"])

    #added 1 day to the upper end of date range, because upper end is exclusive
    if removal_date_max_query != '' and removal_date_max_query is not None and removal_date_min_query == '':
        qs = qs.filter(removal_date__range=["1000-01-01", datetime.strptime(removal_date_max_query, "%Y-%m-%d").date() + timedelta(days=1)])


    if removal_date_min_query != '' and removal_date_max_query != '' and removal_date_min_query < removal_date_max_query:
        qs = qs.filter(publish_date__range=[publish_date_min_query, datetime.strptime(publish_date_max_query, "%Y-%m-%d").date() + timedelta(days=1)])

    else:
        removal_date_min_query = ''
        removal_date_max_query = ''

    #after clicking search button, we save the queries in a dictionary to keep them in their fields
    ql = {"title":title_query, "abstract":abstract_query, "publish_date_min":publish_date_min_query, "publish_date_max":publish_date_max_query, "removal_date_min": removal_date_min_query, "removal_date_max": removal_date_max_query}

    #this dictionary will be passed to posts.html (and homepage.html since posts.html extends it)
    context = {
        "object_list": qs,
        "query_list": ql
    }

    return render(request, "blogs/posts.html", context)
