from django.contrib import admin

# Register your models here.
from image_cropping import ImageCroppingMixin

from apps.blog.models import Post, Category, IPAddress, PostHit


class PostAdmin(admin.ModelAdmin, ImageCroppingMixin):
    list_display = ['img_tag', 'caption', 'location', 'created', 'status', 'author']


admin.site.register(Post, PostAdmin)


class CategoryAdmin(admin.ModelAdmin, ImageCroppingMixin):
    list_display = ['title', 'thumbnail_url']


admin.site.register(Category, CategoryAdmin)
admin.site.register(IPAddress)
admin.site.register(PostHit)

