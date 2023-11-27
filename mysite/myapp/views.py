from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # Добавьте любую дополнительную логику здесь, если необходимо
    return render(request, 'myapp/index.html')

def contacts(request):
    # Добавьте любую дополнительную логику здесь, если необходимо
    return render(request, 'myapp/contacts.html')

def shop(request):
    # Добавьте любую дополнительную логику здесь, если необходимо
    return render(request, 'myapp/shop.html')

def about(request):
    # Добавьте любую дополнительную логику здесь, если необходимо
    return render(request, 'myapp/about.html')
