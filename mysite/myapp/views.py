from django.shortcuts import render
from django.http import HttpResponse
from .models import Products

# Create your views here.

def index(request):
    return render(request, 'myapp/index.html')

def contacts(request):
    return render(request, 'myapp/contacts.html')

def shop(request):
    return render(request,'myapp/shop.html')

def about(request):
    return render(request, 'myapp/about.html')

def cabinet(request):
    return render(request,'myapp/cabinet.html')

def register(request):
    return render(request, 'myapp/register.html')


