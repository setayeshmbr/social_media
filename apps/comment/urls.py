from django.urls import path

from apps.comment.views import DeleteComment

app_name = 'comment'
urlpatterns = [
    path('comment/delete/<int:pk>/' , DeleteComment.as_view() , name= 'comment-delete'),
]