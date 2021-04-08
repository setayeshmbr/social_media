from django.urls import path

from account.views import home

app_name = 'account'
urlpatterns = [
    path('', home, name='home'),
]
