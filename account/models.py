from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from account.managers import MyUserManager


class MyUser(AbstractBaseUser) :
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
    )
    is_superuser = models.BooleanField(default=False)
    username_validator = UnicodeUsernameValidator()

    user_name = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique' : _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    phone_number = models.CharField(_('Phone number'), max_length=11, blank=True, null=True, unique=True)

    class Meta :
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self) :
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self) :
        return self.email

    def has_perm(self, perm, obj=None) :
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label) :
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True




