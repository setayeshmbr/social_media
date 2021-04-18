# from django.urls import path
#
# from apps.blog.views import home
from django.urls import path

from apps.account.views import PostList

app_name = 'account'
urlpatterns = [
    path('post_list', PostList.as_view(), name='post_list'),
]