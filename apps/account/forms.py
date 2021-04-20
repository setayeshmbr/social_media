from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.forms import EmailField
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

from apps.account.models import MyUser


class UserCreationForm(forms.ModelForm) :
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta :
        model = MyUser
        fields = ('email','user_name','phone_number','authenticate_with')

    def clean_password2(self) :
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2 :
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True) :
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit :
            user.save()
        return user


class UserChangeForm(forms.ModelForm) :
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta :
        model = MyUser
        fields = ('email', 'password', 'is_staff')

    def clean_password(self) :
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class CustomAuthenticationForm(forms.Form) :
    email = EmailField(widget=forms.TextInput(attrs={'autofocus' : True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete' : 'current-password'}),
    )

    error_messages = {
        'invalid_login' : _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive' : _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs) :
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.email_field = MyUser._meta.get_field(MyUser.USERNAME_FIELD)
        email_max_length = self.email_field.max_length or 254
        self.fields['email'].max_length = email_max_length
        self.fields['email'].widget.attrs['maxlength'] = email_max_length
        if self.fields['email'].label is None :
            self.fields['email'].label = capfirst(self.email_field.verbose_name)

    def clean(self) :
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password :
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None :
                raise self.get_invalid_login_error()
            else :
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user) :
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active :
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self) :
        return self.user_cache

    def get_invalid_login_error(self) :
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'email' : self.email_field.verbose_name},
        )

class ProfileUpdateForm(forms.ModelForm) :

    def __init__(self, *args, **kwargs) :
        user = kwargs.pop('user')
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

        if not user.is_superuser :
            self.fields['user_name'].disabled = True
            self.fields['email'].disabled = False

    class Meta :
        model = MyUser
        fields = [
            'user_name', 'email', 'first_name', 'last_name','phone_number','image','gender','website','bio'
        ]




