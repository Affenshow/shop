from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.postgres.search import SearchQuery
from django.db.models import Q, Sum, Count, Avg
from django.db.models.functions import TruncMonth
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
import stripe

from .models import (
    Products, ProductsCategory, Basket,
    ProductRating, Order, OrderItem, Review, Feedback
)
from .forms import (
    ProductRatingForm, FeedbackForm, ReviewForm,
    OrderForm
)

stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    return render(request, 'myapp/index.html')


@login_required
def contacts(request):
    form = FeedbackForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Спасибо! Ваше сообщение отправлено.")
        return redirect('myapp:contacts')
    return render(request, 'myapp/contacts.html', {'form': form})


def shop(request, category_name=None):
    categories = ProductsCategory.objects.all()
    products = Products.objects.all()

    selected_ratings = request.GET.getlist('rating')
    if selected_ratings:
        products = products.filter(reviews__rating__in=selected_ratings).distinct()

    if category_name:
        category = get_object_or_404(ProductsCategory, name=category_name)
        products = products.filter(category=category)

    return render(request, 'myapp/shop.html', {
        'title': 'Croup - Товары',
        'categories': categories,
        'products': products,
        'selected_ratings': selected_ratings,
    })


def about(request):
    return render(request, 'myapp/about.html')


@login_required
def basket_add(request, product_id):
    referer = request.META.get('HTTP_REFERER', '/')
    product = get_object_or_404(Products, id=product_id)
    basket, created = Basket.objects.get_or_create(user=request.user, product=product)
    if not created:
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(referer)


@login_required
def basket_delete(request, id):
    basket = get_object_or_404(Basket, id=id, user=request.user)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def add_rating(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    form = ProductRatingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        existing = ProductRating.objects.filter(user=request.user, product=product)
        if existing.exists():
            messages.warning(request, 'Вы уже оценили этот продукт.')
        else:
            ProductRating.objects.create(
                user=request.user,
                product=product,
                rating=form.cleaned_data['rating']
            )
            messages.success(request, 'Спасибо за вашу оценку!')
    return redirect('myapp:shop')


def product_search(request):
    q = request.GET.get('q', '')
    products = Products.objects.filter(
        Q(name__icontains=q) | Q(description__icontains=q)
    ) if q else []
    return render(request, 'myapp/product_search.html', {
        'products': products,
        'query': q,
    })


@login_required
def basket_view(request):
    baskets = Basket.objects.filter(user=request.user)
    total_quantity = sum(b.quantity for b in baskets)
    total_sum = sum(b.get_total_price() for b in baskets)
    return render(request, 'myapp/basket.html', {
        'baskets': baskets,
        'total_quantity': total_quantity,
        'total_sum': total_sum,
    })


@login_required
def checkout(request):
    baskets = Basket.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in baskets)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total
            order.save()
            for item in baskets:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            baskets.delete()
            return redirect('myapp:order_success', order_id=order.id)
    else:
        form = OrderForm(initial={'total_price': total})

    return render(request, 'myapp/checkout.html', {
        'form': form,
        'basket': baskets,
        'total_sum': total,
    })


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'myapp/order_success.html', {'order': order})


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Products, pk=pk)
    reviews = product.reviews.all()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={
                    'rating': form.cleaned_data['rating'],
                    'comment': form.cleaned_data['comment']
                }
            )
            return redirect('myapp:product_detail', pk=pk)
    else:
        form = ReviewForm()
    return render(request, 'myapp/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
    })


@login_required
def create_checkout_session(request):
    baskets = Basket.objects.filter(user=request.user)
    if not baskets.exists():
        return redirect('myapp:shop')

    line_items = [{
        'price_data': {
            'currency': 'usd',
            'product_data': {'name': item.product.name},
            'unit_amount': int(item.product.price * 100),
        },
        'quantity': item.quantity,
    } for item in baskets]

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('myapp:checkout_success')
        ) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('myapp:shop')),
        metadata={'user_id': request.user.id},
    )
    return redirect(session.url, code=303)


@login_required    # можете убрать, если хотите разрешить анонимный доступ
def checkout_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        messages.error(request, "Ошибка: отсутствует идентификатор сессии Stripe.")
        return render(request, 'myapp/checkout_success.html')

    try:
        # Попадание в view и получение данных сессии
        session = stripe.checkout.Session.retrieve(session_id)
        # Создаём заказ
        handle_checkout_session(session)
        messages.success(request, "✅ Ваш заказ был успешно зарегистрирован!")
    except Exception as e:
        # В случае какой-либо ошибки — сохраняем её текст
        messages.error(request, f"Ошибка при создании заказа: {e}")
    return render(request, 'myapp/checkout_success.html')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponseBadRequest()

    if event['type'] == 'checkout.session.completed':
        handle_checkout_session(event['data']['object'])
    return HttpResponse(status=200)


def handle_checkout_session(session):
    user_id = session.metadata.get('user_id')
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.get(id=user_id)

    baskets = Basket.objects.filter(user=user)
    total = sum(item.get_total_price() for item in baskets)

    order = Order.objects.create(
        user=user,
        total_price=total,
    )
    for item in baskets:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
    baskets.delete()


@staff_member_required
def analytics(request):
    # Общие метрики
    total_orders    = Order.objects.count()
    total_revenue   = Order.objects.aggregate(sum=Sum('total_price'))['sum'] or 0
    avg_order_value = Order.objects.aggregate(avg=Avg('total_price'))['avg'] or 0

    # Топ-5 продуктов
    top_products = (
        Products.objects
                .annotate(sold=Sum('order_items__quantity'))
                .filter(sold__gt=0)
                .order_by('-sold')[:5]
    )

    # Продажи по месяцам
    monthly_qs = (
        Order.objects
             .annotate(month=TruncMonth('created_timestamp'))
             .values('month')
             .annotate(revenue=Sum('total_price'), orders=Count('id'))
             .order_by('month')
    )

    # Последние 5 заказов
    last_orders = Order.objects.order_by('-created_timestamp')[:5]

    # Формируем JSON-массивы для Chart.js
    labels = [entry['month'].strftime('%Y-%m') for entry in monthly_qs]
    dataRev = [float(entry['revenue'] or 0) for entry in monthly_qs]
    dataOrd = [entry['orders'] for entry in monthly_qs]

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'avg_order_value': avg_order_value,
        'top_products': top_products,
        'monthly': monthly_qs,
        'last_orders': last_orders,
        'labels_json': json.dumps(labels),
        'dataRev_json': json.dumps(dataRev),
        'dataOrd_json': json.dumps(dataOrd),
    }
    return render(request, 'myapp/analytics.html', context)
