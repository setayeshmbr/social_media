# from django.urls import path
#
# from apps.blog.views import home
from django.urls import path

from apps.account.views import PostList, PostCreate

app_name = 'account'
urlpatterns = [
    path('<str:user_name>/', PostList.as_view(), name='profile'),
    path('post_create', PostCreate.as_view(), name='post_create_update'),
]