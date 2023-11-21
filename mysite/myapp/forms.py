
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Введите почту', max_length=100)
    password = forms.CharField(label='Веедите пароль', widget=forms.PasswordInput())  

class RegistrationForm(forms.Form):
    name = forms.CharField(label='Логин', max_length=100)
    email = forms.EmailField(label='Email')
    street = forms.CharField(label='Адрес', max_length=255)
    city = forms.CharField(label='Город', max_length=255) 
    state = forms.CharField(label='Страна', max_length=255)  
    phone = forms.CharField(label='Телефон', max_length=15)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())
 
