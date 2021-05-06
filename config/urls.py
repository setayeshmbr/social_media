"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from apps.account.views import Login, Register, activate, verify

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('verify/', verify, name='verify'),

    path('', include('apps.account.urls')),
    path('', include('apps.blog.urls')),
    path('', include('apps.comment.urls')),
    path('', include('django.contrib.auth.urls')),

    re_path(r'^ratings/', include('star_ratings.urls', namespace='ratings')),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
