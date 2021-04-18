from django.contrib.auth.decorators import login_required

# Create your views here.
from django.shortcuts import render


@login_required(login_url='login')
def home(request):
    context = {
        'message': "hello woooorld"
    }
    return render(request, 'blog/single.html', context)


# def profile(request):
#     context = {
#         'message': "hello woooorld"
#     }
#     return render(request, 'blog/index.html', context)
