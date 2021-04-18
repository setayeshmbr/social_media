from django.contrib.auth.decorators import login_required

# Create your views here.
from django.shortcuts import render
from django.views.generic import ListView

from apps.blog.models import Post


class PostList(ListView):
    model = Post
    template_name = 'blog/single.html'



# def profile(request):
#     context = {
#         'message': "hello woooorld"
#     }
#     return render(request, 'blog/index.html', context)
