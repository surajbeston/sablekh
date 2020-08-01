"""sablekh_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from api.views import UserView, LibraryView, all_files, all_libraries, get_library, FileView, download_files, search, auth_token, change_link, string_to_library, get_tags, hawa
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.generics import ListCreateAPIView
from django.contrib.auth.models import User

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users', UserView.as_view()),
    path('token', auth_token),
    path('token-to', hawa),
    path('library', LibraryView.as_view()),
    path('file', FileView.as_view()),
    path('all-libraries', all_libraries),
    path('all-files', all_files),
    path('get-library', get_library),
    path('download', download_files),
    path('search', search),
    path('change-link', change_link),
    path('link', string_to_library), 
    path('tags', get_tags)
]
