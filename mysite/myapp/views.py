from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import ProductRatingForm
from django.contrib import messages
from myapp.models import Products, ProductsCategory, Basket, ProductRating


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

    if request.method == 'POST':
        form = ProductRatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            user = request.user

            # Проверяем, не оценил ли пользователь уже этот продукт
            existing_rating = ProductRating.objects.filter(user=user, product=product)
            if existing_rating.exists():
                messages.warning(request, 'Вы уже оценили этот продукт.')
            else:
                ProductRating.objects.create(user=user, product=product, rating=rating)
                messages.success(request, 'Спасибо за вашу оценку!')
    else:
        form = ProductRatingForm()

    return redirect('myapp:shop')  # Измените на ваше представление с товарами
