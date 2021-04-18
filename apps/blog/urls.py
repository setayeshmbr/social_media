from django.urls import path

from .views import CategoryList, CategoryDetail, PostDetail

app_name = 'blog'
urlpatterns = [
    path('', CategoryList.as_view(), name='home'),
    path('category_detail/<slug:slug>', CategoryDetail.as_view(), name='category_detail'),

    path('post_detail/<int:pk>', PostDetail.as_view(), name='post_detail'),
]
