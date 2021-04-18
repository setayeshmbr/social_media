from django.db import models
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from image_cropping.fields import ImageRatioField, ImageCropField
from image_cropping.utils import get_backend
from config import settings
# Create your models here.

class Post(models.Model):
    image = models.ImageField(_('Image'), upload_to='uploaded_images')
    # size is "width x height"
    cropping = ImageRatioField('image', '900 x 750',size_warning=True)
    caption = models.TextField(_('Caption'), blank=True)
    location = models.TextField(_('Location'), blank=True)
    created = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now= True)
    STATUS_CHOICES = (
        ('a', _('Archive')),  # Archive
        ('p', _('Publish')),  # Publish

    )
    status = models.CharField(_('Publish status'),max_length=2, choices=STATUS_CHOICES)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def img_tag(self):
        return format_html("<img width=100 height=75 style='border-radius : 5px;' src ='{}'> ".format(self.image.url))
    img_tag.short_description ='Image'

    def thumbnail_url(self):
        thumbnail_url = get_backend().get_thumbnail_url(
            self.image,
            {
                'size': (430, 360),
                'box': self.cropping,
                'crop': True,
                'detail': True,
            }
        )
        return thumbnail_url

