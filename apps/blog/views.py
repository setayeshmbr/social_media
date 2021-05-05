# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from apps.blog.models import Post, Category

# class PostDetail(DetailView):
#     def get_object(self, queryset=None) :
#         pk = self.kwargs.get('pk')
#         return get_object_or_404(Post.objects.all(), pk=pk)

from .models import Post
from apps.comment.forms import CommentForm
from django.shortcuts import render, get_object_or_404


def post_detail(request, slug):
    template_name = 'blog/post_detail.html'
    post = get_object_or_404(Post, slug=slug)
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
