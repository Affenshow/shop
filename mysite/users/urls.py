# users/urls.py
from django.urls import path
from .views import register, login, cabinet, logout_user

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('cabinet/', cabinet, name='cabinet'),
    path('logout/', logout_user, name='logout'),  # Обновленный путь для выхода из аккаунта
]


