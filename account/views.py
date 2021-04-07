from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

# Create your views here.
from account.forms import CustomAuthenticationForm


def home(request) :
    return HttpResponse('<h1>Page was found</h1>')


class Login(FormView) :
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'

    def form_valid(self, form) :
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)

        # Check here if the user is an admin
        if user is not None and user.is_active :
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)
        else :
            return self.form_invalid(form)

    def get_success_url(self) :
        return reverse_lazy('home')
