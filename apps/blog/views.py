from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

@login_required(login_url='login')
def home(request):
    return HttpResponse('<h1>Page was found</h1>')