from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginated_by = 3
    template_name = 'posts/list.html'


def post_detail(req, year, month, day, post):
    post_obj = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day)

    return render(req, 'posts/detail.html', {'post': post_obj})
