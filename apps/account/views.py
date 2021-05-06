from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
# Create your views here.
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from apps.account.forms import CustomAuthenticationForm, ProfileUpdateForm
from .mixins import FormValidMixin, FieldsMixin
from .models import MyUser, UserFollowing
from ..blog.models import Post


class Login(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    success_url = 'account:profile'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)

        # Check here if the user is an admin
        if user is not None and user.is_active:
            login(self.request, user)
            return HttpResponseRedirect(reverse(self.success_url, kwargs={"user_name": user.user_name}))
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


class Profile(ListView):
    model = Post
    template_name = 'blog/profile.html'
    context_object_name = 'user_obj'

    def get_queryset(self):
        global user
        user_name = self.kwargs.get('user_name')
        user = get_object_or_404(MyUser, user_name=user_name)
        queryset = {'posts': user.posts.all(),
                    'follower': UserFollowing.objects.all().filter(to_user=user , accept=True),
                    'following': UserFollowing.objects.all().filter(from_user=user , accept=True),
                    'requests': UserFollowing.objects.all().filter(to_user=user, accept=False)}

        return queryset

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['user'] = user
        return context


class PostCreate(FieldsMixin, FormValidMixin, CreateView):
    model = Post
    template_name = 'blog/post_create_update.html'

    def get_success_url(self):
        user = self.request.user
        user_name = user.user_name
        return reverse_lazy('account:profile', kwargs={"user_name": user_name})


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'registration/profile_update.html'
    form_class = ProfileUpdateForm

    def get_object(self, queryset=None):
        return MyUser.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(ProfileUpdate, self).get_form_kwargs()
        kwargs.update(
            {
                'user': self.request.user
            }
        )
        return kwargs

    def get_success_url(self):
        user_name = self.object.user_name
        return reverse_lazy('account:profile', kwargs={'user_name': user_name})


class Request(LoginRequiredMixin, View):
    def get(self, request, user_name):
        user = self.request.user
        followed = get_object_or_404(MyUser, user_name=user_name)
        if UserFollowing.objects.filter(from_user=user, to_user=followed.pk).count() == 0:
            req = UserFollowing(from_user=user, to_user=followed, accept=False)
            req.save()
        else:
            req = UserFollowing.objects.get(from_user=user, to_user=followed)
            req.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class RequestConfirm(LoginRequiredMixin, View):
    def get(self, request, user_name):
        user = self.request.user
        requested = get_object_or_404(MyUser, user_name=user_name)
        req = UserFollowing.objects.get(from_user=requested, to_user=user , accept=False)
        req.delete()

        req = UserFollowing(from_user=requested, to_user=user, accept=True)
        req.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class RequestDelete(LoginRequiredMixin, View):
    def get(self, request, user_name):
        user = self.request.user
        requested = get_object_or_404(MyUser, user_name=user_name)
        req = UserFollowing.objects.get(from_user=requested, to_user=user)
        req.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class PostUpdate(FieldsMixin, FormValidMixin, UpdateView) :
    model = Post
    template_name = 'blog/post_create_update.html'

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy('account:profile', kwargs={'user_name': user.user_name})


class PostDelete(DeleteView) :
    model = Post
    success_url = reverse_lazy('blog:home')
    template_name = 'registration/post_confirm_delete.html'
    def get_success_url(self):
        user = self.request.user
        return reverse_lazy('account:profile' , kwargs = {'user_name' : user.user_name})