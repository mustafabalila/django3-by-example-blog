from django.urls import path
from .views import PostListView, post_detail

app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         post_detail, name='detail')
]
