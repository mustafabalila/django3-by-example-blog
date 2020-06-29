from django.core.mail import send_mail
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from taggit.models import Tag
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginated_by = 3
    template_name = 'posts/list.html'

    def get(self, request, *args, **kwargs):
        tag_slug = kwargs.get('tag', None)
        if tag_slug:
            tag = get_object_or_404(Tag, slug=kwargs['tag'])
            posts = queryset.filter(tags__in=[tag])
            return render(request, self.template_name, {'posts': posts})
        else:
            return super().get(self, request, *args, **kwargs)


def post_list(req, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = req.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(req,
                  'posts/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag': tag})


def post_detail(req, year, month, day, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day)
    comments = post.comments.all()
    new_comment = None

    if req.method == 'POST':
        comment_form = CommentForm(req.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = req.user
            new_comment.save()
    else:
        comment_form = CommentForm()
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(
            tags__in=post_tags_ids).exclude(id=post.id)

        similar_posts = similar_posts.annotate(
            same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(req, 'posts/detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'similar_posts': similar_posts})


def post_share(req, post_id):
    post = get_object_or_404(Post, id=post_id)
    sent = False
    if req.method == 'POST':
        form = EmailPostForm(req.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_uri = req.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_uri}\n\n"\
                f"{cd['name']}'s comments: {cd['comments']} "
        send_mail(subject, message, 'admin@blog.com', [cd['to']])
        sent = True
    else:
        form = EmailPostForm()
    return render(req, 'posts/share.html', {'form': form, 'post': post, 'sent': sent})


def post_search(req):
    form = SearchForm()
    query = None
    results = []
    if 'query' in req.GET:
        form = SearchForm(req.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector(
                'title', 'weight=A', ) + SearchVector('body', 'weight=B', )
            search_query = SearchQuery(query)
            results = Post.published.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')

    return render(req, 'posts/search.html', {
        'form': form,
        'query': query,
        'results': results})
