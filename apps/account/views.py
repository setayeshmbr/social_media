from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
# Create your views here.
from django.views.generic import CreateView, ListView

from apps.account.forms import CustomAuthenticationForm
from .models import MyUser
from ..blog.models import Post


class Login(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    success_url = 'account:post_list'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)

        # Check here if the user is an admin
        if user is not None and user.is_active:
            login(self.request, user)
            return HttpResponseRedirect(reverse(self.success_url))
        else:
            return self.form_invalid(form)


from django.http import HttpResponse
from .forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from . import helper


class Register(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = 'verify'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True

        current_site = get_current_site(self.request)
        authenticate_status = user.authenticate_with
        if authenticate_status == 'p':
            # send otp
            otp = helper.get_random_otp()
            # helper.send_otp(user.phone_number , otp)
            # save otp
            user.otp = otp
            user.save()
            self.request.session['user_mobile'] = user.phone_number
            return HttpResponseRedirect(reverse(self.success_url))

        elif authenticate_status == 'e':
            user.save()
            # sending email
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # # return redirect('home')
        return HttpResponse(
            'Thank you for your email confirmation. Now you can <a href="/login">login</a> your account.')

    else:
        return HttpResponse('Activation link is invalid! <a href ="/register">Try again</a>')


def verify(request):
    try:
        mobile_number = request.session.get('user_mobile')
        user = get_object_or_404(MyUser, phone_number=mobile_number)

        if request.method == "POST":
            if user.otp != int(request.POST.get('otp')):
                return HttpResponseRedirect(reverse('register'))
            user.is_active = True
            return HttpResponse(
                'Thank you for your confirmation. Now you can <a href="/login">login</a> your account.')
        return render(request, 'registration/acc_active_mobile.html', {'mobile_number': mobile_number})
    except:
        return HttpResponseRedirect(reverse('register'))


class PostList(ListView) :
    model = Post
    template_name = 'blog/post_list.html'

    def get_queryset(self) :
        return self.request.user.posts.all()