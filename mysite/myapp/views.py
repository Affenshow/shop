from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import ProductRatingForm
from .forms import OrderForm
from django.contrib.postgres.search import SearchQuery
from django.db.models import Q
from django.contrib import messages
from myapp.models import Products, ProductsCategory, Basket, ProductRating, Order, OrderItem


def index(request):

    return render(request, 'myapp/index.html')

def contacts(request):

    return render(request, 'myapp/contacts.html')


def shop(request, category_name=None):
    categories = ProductsCategory.objects.all()
    products = Products.objects.all()

    if category_name:
        category = get_object_or_404(ProductsCategory, name=category_name)
        products = products.filter(category=category)
        

    context = {
        'title': 'Croup - Товары',
        'categories': categories,
        'products': products,
    }

    return render(request, 'myapp/shop.html', context)





def about(request):

    return render(request, 'myapp/about.html')


@login_required
def basket_add(request, product_id):
    current_page = request.META.get('HTTP_REFERER')
    product = Products.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
        return HttpResponseRedirect(current_page)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(current_page)
    
@login_required 
def basket_delete(request, id):
    basket = Basket.objects.get(id=id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_rating(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    user = request.user

    if request.method == 'POST':
        form = ProductRatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']

            existing_rating = ProductRating.objects.filter(user=user, product=product)
            if existing_rating.exists():
                messages.warning(request, 'Вы уже оценили этот продукт.')
            else:
                ProductRating.objects.create(user=user, product=product, rating=rating)
                messages.success(request, 'Спасибо за вашу оценку!')

    return redirect('myapp:shop')


def product_search(request):
    query = request.GET.get('q')
    products = []

    if query:
        search_query = SearchQuery(query)
        products = Products.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    context = {'products': products, 'query': query}
    return render(request, 'myapp/product_search.html', context)


def checkout(request):
    basket = Basket.objects.filter(user=request.user)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # Добавьте товары из корзины в OrderItem и рассчитайте итоговую сумму
            total_price = sum(item.sum() for item in basket)
            order.total_price = total_price
            order.save()

            for item in basket:
                order_item = OrderItem(order=order, product=item.product, quantity=item.quantity)
                order_item.save()

            # Очистите корзину пользователя
            basket.delete()

            return render(request, 'myapp/order_success.html', {'order_number': order.id})
    else:
        form = OrderForm()

    return render(request, 'myapp/checkout.html', {'form': form, 'basket': basket})

def order_success(request):
    return render(request, 'myapp/order_success.html')