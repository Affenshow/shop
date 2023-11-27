# users/views.py
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm
from address.forms import AddressForm
from address.models import Address

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        address_form = AddressForm(request.POST)

        if user_form.is_valid() and address_form.is_valid():
            user = user_form.save()
            address = address_form.save(commit=False)
            address.user = user
            address.save()
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        user_form = UserRegistrationForm()
        address_form = AddressForm()

    return render(request, 'users/register.html', {'user_form': user_form, 'address_form': address_form}