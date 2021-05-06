from django.urls import path

from .views import CategoryList, CategoryDetail, post_detail, PostHitsList

app_name = 'blog'
urlpatterns = [
    path('', CategoryList.as_view(), name='home'),
    path('category_detail/<slug:slug>/', CategoryDetail.as_view(), name='category_detail'),

    path('post_detail/<slug:slug>/', post_detail, name='post_detail'),
    path('hits/explore', PostHitsList.as_view(), name='post_list'),
    # path('post_detail/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
]
