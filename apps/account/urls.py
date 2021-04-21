# from django.urls import path
#
# from apps.blog.views import home
from django.urls import path

from apps.account.views import Profile, PostCreate, ProfileUpdate, FollowingList, FollowerList

app_name = 'account'
urlpatterns = [
    path('<str:user_name>/', Profile.as_view(), name='profile'),
    path('post_create', PostCreate.as_view(), name='post_create_update'),
    path('account/profile/', ProfileUpdate.as_view(), name='profile-update'),

    # path('<str:user_name>/followers', Profile.as_view(), name='profile'),
    path('<str:user_name>/followings', FollowingList.as_view(), name='following_list'),
    path('<str:user_name>/followers', FollowerList.as_view(), name='follower_list'),
]
