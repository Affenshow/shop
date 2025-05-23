# users/views.py
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import User
from myapp.models import Basket, Feedback

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return HttpResponseRedirect(reverse('myapp:index'))
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)

            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('users:cabinet'))
    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request, 'users/login.html', context)

@login_required
@login_required
def cabinet(request):
    # Обработка обновления профиля
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:cabinet')
    else:
        form = UserProfileForm(instance=request.user)
    
    # Корзина
    baskets = Basket.objects.filter(user=request.user)
    total_quantity = sum(b.quantity for b in baskets)
    total_sum = sum(item.get_total_price() for item in baskets)
    
    # Ваши обращения (feedback)
    feedbacks = Feedback.objects.filter(email=request.user.email).order_by('-created')
    
    context = {
        'form': form,
        'title': 'Croup - Личный кабинет',
        'baskets': baskets,
        'total_quantity': total_quantity,
        'total_sum': total_sum,
        'feedbacks': feedbacks,        # <-- Передаём в шаблон
    }
    return render(request, 'users/cabinet.html', context)



def logout_user(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))

