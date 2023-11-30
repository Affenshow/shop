# users/views.py
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import User

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
                return HttpResponseRedirect(reverse('myapp:index'))
    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request, 'users/login.html', context)

@login_required
def cabinet(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:cabinet')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {'form': form}
    return render(request, 'users/cabinet.html', context)    


def logout_user(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))

