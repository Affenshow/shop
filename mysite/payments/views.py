import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

def stripe_checkout(request):
    if request.method == 'POST':
        # Пример: динамическая сумма заказа
        from myapp.models import Basket
        baskets = Basket.objects.filter(user=request.user)
        total_sum = sum(item.get_total_price() for item in baskets)
        unit_amount = int(total_sum * 100)  # переводим в минимальные единицы

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'kzt',  # Валюта KZT
                    'product_data': {
                        'name': f'Заказ пользователя {request.user.username}',
                    },
                    'unit_amount': unit_amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/payments/payment-success/'),
            cancel_url=request.build_absolute_uri('/payments/payment-cancel/'),
        )
        return redirect(session.url, code=303)
    return render(request, 'payments/stripe_checkout.html')

def payment_success(request):
    return render(request, 'payments/payment_success.html')

def payment_cancel(request):
    return render(request, 'payments/payment_cancel.html')
