from django.urls import path, re_path, include
from django.views.generic import ListView, DetailView
from . import views
from blogs.models import Blog

urlpatterns = [
    #path('', views.homepage),
    path('addblog/', views.add_blog),
    path('deleteblog/<int:pk>/', views.delete_blog, name='delete_blog'),
    path('', ListView.as_view(queryset=Blog.objects.all().order_by('-publish_date'), template_name = 'blogs/posts.html')),
    path('blogs/<int:pk>/', DetailView.as_view(model=Blog, template_name='blogs/post.html')),
    path('editblog/<int:pk>/', views.edit_blog, name='edit_blog'),
    path('search/', views.search)
]
