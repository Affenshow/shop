from django.urls import path
from myapp.views import index, contacts, shop, about

app_name = 'myapp'

urlpatterns = [
    path("index/", index, name="index"),
    path("contacts/", contacts, name="contacts"),
    path("shop/", shop, name="shop"),
    path("about/", about, name="about"),

]
