from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

# Create your views here.
from account.forms import CustomAuthenticationForm


@login_required(login_url='login')
def home(request) :
    return HttpResponse('<h1>Page was found</h1>')


class Login(LoginView) :
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    success_url = 'account:home'

    def form_valid(self, form) :
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)

        # Check here if the user is an admin
        if user is not None and user.is_active :
            login(self.request, user)
            return HttpResponseRedirect(reverse(self.success_url))
        else :
            return self.form_invalid(form)

