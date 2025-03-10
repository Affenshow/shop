from django.urls import path
from .views import stripe_checkout, payment_success, payment_cancel

app_name = 'payments'

urlpatterns = [
    path('stripe-checkout/', stripe_checkout, name='stripe_checkout'),
    path('payment-success/', payment_success, name='payment_success'),
    path('payment-cancel/', payment_cancel, name='payment_cancel'),
]
