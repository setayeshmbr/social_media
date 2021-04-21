from django.conf import settings
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
    image = models.ImageField(_('Image'), upload_to='profile_photo', blank=True, null=True,
                              default='profile_photo/default_profile.png')
    GENDER = [('f', _('Female')), ('m', _('Male'))]
    gender = models.CharField(_('Gender'), max_length=2, choices=GENDER, blank=True, null=True)
    website = models.CharField(_('Website'), blank=True, max_length=150, validators=[validate_website_url])
    bio = models.TextField(_('Bio'), blank=True, max_length=100)
    STATUS_CHOICES = (
        ('p', _('Phone number')),
        ('e', _('Email'))
    )
    authenticate_with = models.CharField(choices=STATUS_CHOICES, max_length=1)

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

    otp = models.PositiveIntegerField(blank=True, null=True)
    otp_create_time = models.DateTimeField(auto_now=True)

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

    # @property
    # def following(self):
    #     following = []
    #     for obj in UserFollowing.objects.filter(from_user=self, accept=True):
    #         following.append(obj.to_user.id)
    #     following = MyUser.objects.filter(id__in=following)
    #     return following
    #
    # @property
    # def followers(self):
    #
    #     followers = []
    #     for obj in UserFollowing.objects.filter(to_user=self, accept=True):
    #         followers.append(obj.from_user.id)
    #     followers = MyUser.objects.filter(id__in=followers)
    #     return followers


class UserFollowing(models.Model):
    from_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='followings', on_delete=models.CASCADE)
    to_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)
    accept = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['created']

    # def __str__(self):
    #     return self.from_user.user_name + ' request to  ' + self.to_user.user_name + str(self.accept)

    # def __str__(self):
    #     f"{self.user_id} follows {self.following_user_id}"
