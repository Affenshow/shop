# urls.py
from django.urls import path
from .views import index, contacts, shop, about, basket_add, basket_delete, add_rating

app_name = 'myapp'

urlpatterns = [
    path("index/", index, name="index"),
    path("contacts/", contacts, name="contacts"),
    path("shop/", shop, name="shop"),
    path('shop/<str:category_name>/', shop, name='shop_by_category'),
    path('basket-add/<int:product_id>/', basket_add, name='basket_add'),
    path('basket-delete/<int:id>/', basket_delete, name='basket_delete'),
    path('add_rating/<int:product_id>/', add_rating, name='add_rating'),
    path("about/", about, name="about"),
]
