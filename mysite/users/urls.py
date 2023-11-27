# users/urls.py
from django.urls import path
from .views import register, login, cabinet

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('cabinet/', cabinet, name='cabinet'),
]

