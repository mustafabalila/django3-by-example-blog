from django.urls import path
from django.contrib.sitemaps.views import sitemap
from .views import post_list, post_detail, post_share, post_search
from .sitemaps import PostSitemap
from .feeds import LatestPostsFeed

app_name = 'posts'

sitemaps = {'posts': PostSitemap}

urlpatterns = [
    path('', post_list, name='list'),
    path('tag/<slug:tag_slug>/', post_list, name='tagged'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         post_detail, name='detail'),
    path('<int:post_id>', post_share, name='share'),
    path('sitemap.xml', sitemap, {
         'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemaps'),
    path('feed/', LatestPostsFeed(), name='feed'),
    path('search/', post_search, name='search'),
]
