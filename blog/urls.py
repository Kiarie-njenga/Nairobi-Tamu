





from django.urls import include, path

from . import views
from .feeds import AtomSiteNewsFeed, LatestPostsFeed

urlpatterns = [
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("feed/atom", AtomSiteNewsFeed()),
    path("", views.post_list, name="home"),
    # path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path("<slug:slug>/", views.post_detail, name="post_detail"),
    path('create/post/', views.BlogCreateView.as_view(), name="create_blog"),
    path('<slug:slug>/edit', views.BlogEditView.as_view(), name="edit_blog"),
    path('<slug:slug>/delete', views.BlogDeleteView.as_view(), name="delete_blog"),
    path('search', views.BlogSearch.as_view(), name='blog_search'),
    path('<int:pk>/', views.cat_detail, name='category_detail'),
    path('about', views.About.as_view(), name='about'),
    path('services', views.Service.as_view(), name='services'),
    
    path('categories/<str:title>/', views.cat_tag_search, name='categories'),
]
