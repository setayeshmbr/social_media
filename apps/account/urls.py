# from django.urls import path
#
# from apps.blog.views import home
from django.urls import path, re_path

from apps.account.views import Profile, PostCreate, ProfileUpdate, Request

app_name = 'account'
urlpatterns = [
    path('<str:user_name>/', Profile.as_view(), name='profile'),
    path('post_create', PostCreate.as_view(), name='post_create_update'),
    path('account/profile/', ProfileUpdate.as_view(), name='profile-update'),
    path(r'request/<str:user_name>/', Request.as_view(), name='request'),
]
