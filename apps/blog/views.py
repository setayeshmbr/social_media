# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from apps.blog.models import Post, Category


class PostDetail(DetailView):
    def get_object(self, queryset=None) :
        pk = self.kwargs.get('pk')
        return get_object_or_404(Post.objects.all(), pk=pk)


class CategoryList(LoginRequiredMixin,ListView):
    model = Category
    template_name = 'blog/category_list.html'


class CategoryDetail(ListView):
    template_name = 'blog/category_detail.html'
    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug = slug)
        return category.posts.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryDetail, self).get_context_data( **kwargs)
        context['category'] = category
        return context