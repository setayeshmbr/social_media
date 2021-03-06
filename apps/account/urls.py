# from django.urls import path
#
# from apps.blog.views import home
from django.urls import path, re_path

from apps.account.views import Profile, PostCreate, ProfileUpdate, Request, RequestConfirm, RequestDelete, PostDelete, \
    PostUpdate

app_name = 'account'
urlpatterns = [
    path('<str:user_name>/', Profile.as_view(), name='profile'),
    path('post/create/', PostCreate.as_view(), name='post_create_update'),
    path('account/profile/', ProfileUpdate.as_view(), name='profile-update'),
    path(r'request/<str:user_name>/', Request.as_view(), name='request'),
    path(r'requestconfirm/<str:user_name>/', RequestConfirm.as_view(), name='request-confirm'),
    path(r'requestdelete/<str:user_name>/', RequestDelete.as_view(), name='request-delete'),
    path('post/update/<int:pk>/', PostUpdate.as_view(), name='post-update'),
    path('post/delete/<int:pk>/', PostDelete.as_view(), name='post-delete'),
]