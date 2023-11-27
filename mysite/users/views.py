# users/views.py
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import User
from Address.models import Address
from Address.forms import AddressForm

def login(request):
    context = {}

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(request, username=username, password=password)

            if user and user.is_active:
                auth.login(request, user)
                next_url = request.GET.get('next', reverse('myapp:index'))
                return redirect(next_url)
    else:
        form = UserLoginForm()

    context['form'] = form
    return render(request, 'users/login.html', context)

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            Address = profile_form.save(commit=False)
            Address.user = user
            Address.save()
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def cabinet(request):
    user = request.user
    Address = user.Address  # Обратите внимание, что теперь используется user.address

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user)
        address_form = AddressForm(request.POST, instance=Address)
        if profile_form.is_valid() and address_form.is_valid():
            profile_form.save()
            address_form.save()
    else:
        profile_form = UserProfileForm(instance=user)
        address_form = AddressForm(instance=Address)

    return render(request, 'users/cabinet.html', {'profile_form': profile_form, 'Address_form': address_form})



