from django.urls import path
from .views import post_list, post_detail, post_share

app_name = 'posts'

urlpatterns = [
    path('', post_list, name='list'),
    path('tag/<slug:tag_slug>/', post_list, name='tagged'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         post_detail, name='detail'),
    path('<int:post_id>', post_share, name='share')
]
