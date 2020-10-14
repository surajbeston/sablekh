from django.contrib import admin
from django.urls import path
from api.views import UserView, LibraryView, all_files, all_libraries, get_library, FileView, download_files, search, auth_token, change_link, string_to_library, get_tags
from api.views import send_password_key, reset_password, like, all_likes, check_like, all_downloads, home, LibraryGroupView, all_library_groups, get_library_group
from api.views import FavouriteLibraryView, FavouriteLibraryGroupView, check_favourite_library, check_favourite_library_group, verify_email
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.generics import ListCreateAPIView
from django.contrib.auth.models import User

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('users', UserView.as_view()),
    path('token', auth_token),
    path('library', LibraryView.as_view()),
    path('file', FileView.as_view()),
    path('all-libraries', all_libraries),
    path('all-files', all_files),
    path('all-libraries', all_libraries),
    path('get-library', get_library),
    path('download', download_files),
    path('search', search),
    path('change-link', change_link),
    path('link', string_to_library), 
    path('send-password-key', send_password_key),
    path('reset-password', reset_password),
    path('verify-email', verify_email),
    path('like', like),
    path('all-likes', all_likes),
    path('check-like', check_like),
    path('all-downloads', all_downloads),
    path('tags', get_tags),
    path('library-group', LibraryGroupView.as_view()),
    path('all-library-groups', all_library_groups),
    path('get-library-group', get_library_group),
    path('favourite-library', FavouriteLibraryView.as_view()),
    path('favourite-library-group', FavouriteLibraryGroupView.as_view()),
    path('check-favourite-library', check_favourite_library),
    path('check-favourite-library-group', check_favourite_library_group)
]
