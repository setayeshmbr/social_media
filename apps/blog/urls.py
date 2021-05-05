from django.urls import path

from .views import CategoryList, CategoryDetail, post_detail

app_name = 'blog'
urlpatterns = [
    path('', CategoryList.as_view(), name='home'),
    path('category_detail/<slug:slug>/', CategoryDetail.as_view(), name='category_detail'),

    path('post_detail/<slug:slug>/', post_detail, name='post_detail'),
]
