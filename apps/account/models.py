from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.account.managers import MyUserManager
from apps.account.validators import UnicodeMobileNumberValidator, validate_website_url


class MyUser(AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()
    mobile_number_validator = UnicodeMobileNumberValidator()

    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    user_name = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
    )
    phone_number = models.CharField(
        _('Phone number'),
        max_length=11,
        blank=True,
        null=True,
        unique=True,
        validators=[mobile_number_validator],
        error_messages={
            'unique': _("A user with that mobile number already exists."),
        },
    )
    image = models.ImageField(_('Image'), upload_to='profile_photo', blank=True, null=True)
    GENDER = [('f', _('Female')), ('m', _('Male'))]
    gender = models.CharField(_('Gender'), max_length=2, choices=GENDER, blank=True, null=True)
    website = models.CharField(_('Website'), blank=True, max_length=150,validators=[validate_website_url])


    STATUS_CHOICES =(
        ('p', _('Phone number')),
        ('e' ,_('Email'))
    )
    authenticate_with =models.CharField(choices=STATUS_CHOICES , max_length=1)


    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )




    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class PhoneModel(models.Model):
    Mobile = models.IntegerField(blank=False)
    isVerified = models.BooleanField(blank=False, default=False)
    counter = models.IntegerField(default=0, blank=False)


def __str__(self):
    return str(self.Mobile)
