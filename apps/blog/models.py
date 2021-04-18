# from django.db import models
# from django.utils.translation import ugettext_lazy as _
# from config import settings
# # Create your models here.
#
# class Post(models.Model):
#     image = models.ImageField(_('Image'),upload_to='post_images')
#     caption = models.TextField(_('Caption'), blank=True)
#     location = models.TextField(_('Location'), blank=True)
#     created = models.DateTimeField(auto_now_add= True)
#     updated = models.DateTimeField(auto_now= True)
#     STATUS_CHOICES = (
#         ('a', _('Archive')),  # Archive
#         ('p', _('Publish')),  # Publish
#
#     )
#     status = models.CharField(_('Publish status'),max_length=2, choices=STATUS_CHOICES)
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
