from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm
from .models import UserProfile, Address

# Create your views here.

def index(request):
    return render(request, 'myapp/index.html')

def contacts(request):
    return render(request, 'myapp/contacts.html')

def shop(request):
    return render(request,'myapp/shop.html')

def about(request):
    return render(request, 'myapp/about.html')

@login_required
def cabinet(request):
    user = request.user
    try:
        profile = user.userprofile
        context = {
            'username': user.first_name or user.username,
            'user': user,
            'phone': getattr(profile, 'phone', 'Phone not available'),
            'city': getattr(profile.address, 'city', 'City not available'),
            'state': getattr(profile.address, 'state', 'State not available'),
        }
    except UserProfile.DoesNotExist:
        context = {
            'username': user.first_name or user.username,
            'user': user,
            'phone': 'Phone not available',
            'city': 'City not available',
            'state': 'State not available',
        }

    return render(request, 'myapp/cabinet.html', context)






def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Извлекаем данные из формы
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            street = form.cleaned_data['street']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            # Проверяем, что пароли совпадают
            if password == confirm_password:
                # Создаем пользователя
                user = User.objects.create_user(username=email, email=email, password=password)
                # Присваиваем значения дополнительным полям
                user.first_name = name
                user.save()

                # Создаем профиль пользователя
                UserProfile.objects.create(user=user, phone=phone, address=Address.objects.create(street=street, city=city, state=state))

                # Перенаправляем на страницу входа после успешной регистрации
                return redirect('login')
            else:
                form.add_error('confirm_password', 'Пароли не совпадают')

    else:
        form = RegistrationForm()

    return render(request, 'myapp/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Обработка данных формы, например, вход пользователя
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('cabinet')  # Перенаправление на кабинет после успешного входа
            else:
                form.add_error('username', 'Неверное имя пользователя или пароль')

    else:
        form = LoginForm()

    return render(request, 'myapp/login.html', {'form': form})

@login_required
def cabinet(request):
    user = request.user
    context = {
        'username': user.first_name or user.username,  # Пытаемся использовать имя, если оно указано, в противном случае используем имя пользователя
        'user': user,
    }
    return render(request, 'myapp/cabinet.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')  # Перенаправление на главную страницу или другую страницу после выхода