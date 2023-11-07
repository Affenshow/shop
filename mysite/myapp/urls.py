from django.urls import path
from myapp.views import index, contacts, shop, about, cabinet, register
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("index.html/", index, name="index"),
    path("contacts.html/", contacts, name="contacts"),
    path("shop.html/", shop, name="shop"),
    path("about.html/", about, name="about"),
    path("cabinet.html/", cabinet, name="cabinet"),
    path("register.html/", register, name="register"),
]
