from django.urls import path
from .views import index, contacts, shop, about, basket_add, basket_delete, add_rating, product_search, checkout, order_success, basket_view

app_name = 'myapp'

urlpatterns = [
    path("index/", index, name="index"),
    path("contacts/", contacts, name="contacts"),
    path("shop/", shop, name="shop"),
    path('shop/<str:category_name>/', shop, name='shop_by_category'),
    path('basket-add/<int:product_id>/', basket_add, name='basket_add'),
    path('basket-delete/<int:id>/', basket_delete, name='basket_delete'),
    path('add_rating/<int:product_id>/', add_rating, name='add_rating'),
    path('search/', product_search, name='product_search'),
    path('basket/', basket_view, name='basket_view'),
    path("about/", about, name="about"),
]
