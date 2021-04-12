from django.urls import path

from apps.account.views import home

app_name = 'account'
urlpatterns = [
    path('', home, name='home'),
]
