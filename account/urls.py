from django.urls import path

from account.views import home, index

app_name = 'account'
urlpatterns = [
    path('', home, name='home'),
    path('', index, name='index'),
]
