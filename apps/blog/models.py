from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from image_cropping.fields import ImageRatioField
from image_cropping.utils import get_backend

from config import settings


# Create your models here.


def slugify_function(content):
    return slugify(content, allow_unicode=True)


class Category(models.Model):
    image = models.ImageField(_('Image'), upload_to='category_images')
    # size is "width x height"
    cropping = ImageRatioField('image', '900 x 874', size_warning=True)
    title = models.CharField(_('Title'), max_length=30)
    slug = AutoSlugField(populate_from=['title'], unique=True, allow_unicode=True, slugify_function=slugify_function)

    def thumbnail_url(self):
        thumbnail_url = get_backend().get_thumbnail_url(
            self.image,
            {
                'size': (900, 874),
                'box': self.cropping,
                'crop': True,
                'detail': True,
            }
        )
        return thumbnail_url

    def __str__(self):
        return self.title


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='IP Address')

    def __str__(self):
        return self.ip_address


class Post(models.Model):
    title = models.CharField(_('Title'), max_length=30, blank=True)
    slug = AutoSlugField(populate_from=['title'], unique=True, allow_unicode=True, slugify_function=slugify_function)
    image = models.ImageField(_('Image'), upload_to='uploaded_images')
    # size is "width x height"
    cropping = ImageRatioField('image', '900 x 750', size_warning=True)
    caption = models.TextField(_('Caption'), max_length=1024, blank=True)
    location = models.CharField(_('Location'), blank=True, max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = (
        ('a', _('Archive')),  # Archive
        ('p', _('Publish')),  # Publish

    )
    status = models.CharField(_('Publish status'), max_length=2, choices=STATUS_CHOICES, blank=True, default='p')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts', null=True)
    category = models.ManyToManyField(Category, verbose_name=_('Category'), related_name='posts', blank=True, null=True)
    hits = models.ManyToManyField(IPAddress, through='PostHit', blank=True, related_name='hits', verbose_name='views')

    def img_tag(self):
        return format_html("<img width=100 height=75 style='border-radius : 5px;' src ='{}'> ".format(self.image.url))

    img_tag.short_description = 'Image'

    def thumbnail_url(self):
        thumbnail_url = get_backend().get_thumbnail_url(
            self.image,
            {
                'size': (900, 750),
                'box': self.cropping,
                'crop': True,
                'detail': True,
            }
        )
        return thumbnail_url

    def __str__(self):
        return self.title


class PostHit(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  '({}) viewed post : {}'.format(self.ip_address, self.post.title)
