from django.contrib import admin

# Register your models here.
from image_cropping import ImageCroppingMixin

from apps.blog.models import Post


class PostAdmin(admin.ModelAdmin,ImageCroppingMixin):
    list_display = ['img_tag', 'caption', 'location', 'created', 'status', 'author']


admin.site.register(Post, PostAdmin)
