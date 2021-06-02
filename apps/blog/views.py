# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from datetime import datetime, timedelta
from apps.blog.models import Category
from apps.comment.forms import CommentForm
from .models import Post
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@login_required
def post_detail(request, slug):
    template_name = 'blog/post_detail.html'

    if cache.get(slug):
        post = cache.get(slug)
    else:
        try:
            post = get_object_or_404(Post, slug=slug)
            cache.set(slug, post)
        except Post.DoesNotExist:
            return redirect('/')

    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.email = request.user.email
            new_comment.active = True

            new_comment.save()
    else:
        ip_address = request.user.ip_address
        if ip_address not in post.hits.all():
            post.hits.add(ip_address)
        comment_form = CommentForm()

    return render(request, template_name, {'object': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'form': comment_form})


class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'blog/category_list.html'


class CategoryDetail(ListView):
    template_name = 'blog/category_detail.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=slug)
        return category.posts.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        context['category'] = category
        return context


class PostHitsList(ListView):
    last_month = datetime.today() - timedelta(days=30)
    model = Post
    template_name = 'blog/post_hits_list.html'
    queryset = Post.objects.annotate(count=Count('hits', filter=Q(posthit__created__gt=last_month))).order_by('-count',
                                                                                                              '-created')
