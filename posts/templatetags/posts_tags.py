from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
from markdown import markdown
from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('posts/latest_posts.html')
def show_latest_posts(count=6):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def show_most_commented_posts(count=3):
    posts = Post.published.annotate(total_comments=Count(
        'comments')).order_by('-total_comments')[:count]
    return posts


@register.filter('markdown')
def markdown_format(text):
    return mark_safe(markdown(text))
