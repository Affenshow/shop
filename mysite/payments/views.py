import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from myapp.models import Basket, Order, OrderItem
from myapp.views import handle_checkout_session

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def stripe_checkout(request):
    if request.method == 'POST':
        baskets = Basket.objects.filter(user=request.user)
        if not baskets.exists():
            messages.error(request, "Корзина пуста.")
            return redirect('myapp:shop')

        total_sum = sum(item.get_total_price() for item in baskets)
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'kzt',
                    'product_data': {
                        'name': f'Заказ пользователя {request.user.username}',
                    },
                    'unit_amount': int(total_sum * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(
                '/payments/payment-success/'
            ) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri('/payments/payment-cancel/'),
            metadata={'user_id': request.user.id},
        )
        return redirect(session.url, code=303)
    return render(request, 'payments/stripe_checkout.html')


@login_required
def payment_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        messages.error(request, "Не удалось получить session_id от Stripe.")
        return render(request, 'payments/payment_success.html')

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        handle_checkout_session(session)
        messages.success(request, "✅ Ваш заказ оформлен и сохранён.")
    except Exception as e:
        messages.error(request, f"Ошибка при регистрации заказа: {e}")

    return render(request, 'payments/payment_success.html')


@login_required
def payment_cancel(request):
    messages.info(request, "Вы отменили оплату. Заказ не создан.")
    return render(request, 'payments/payment_cancel.html')
