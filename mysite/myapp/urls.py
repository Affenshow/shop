from django.urls import path
from .views import (
    index,
    contacts,
    shop,
    about,
    basket_add,
    basket_delete,
    add_rating,
    product_search,
    basket_view,
    checkout,
    checkout_success,
    order_success,
    product_detail,
    create_checkout_session,
    stripe_webhook,
    analytics
)

app_name = 'myapp'

urlpatterns = [
    path('index/', index, name='index'),
    path('contacts/', contacts, name='contacts'),
    path('shop/', shop, name='shop'),
    path('shop/<str:category_name>/', shop, name='shop_by_category'),

    path('basket/', basket_view, name='basket_view'),
    path('basket-add/<int:product_id>/', basket_add, name='basket_add'),
    path('basket-delete/<int:id>/', basket_delete, name='basket_delete'),

    path('add-rating/<int:product_id>/', add_rating, name='add_rating'),
    path('search/', product_search, name='product_search'),

    path('product/<int:pk>/', product_detail, name='product_detail'),

    # Кассовый процесс
    path('checkout/', checkout, name='checkout'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('checkout-success/', checkout_success, name='checkout_success'),
    path('order-success/<int:order_id>/', order_success, name='order_success'),

    # Webhook Stripe
    path('stripe/webhook/', stripe_webhook, name='stripe-webhook'),

    # Аналитика (только для персонала)
    path('analytics/', analytics, name='analytics'),

    path('about/', about, name='about'),
]
