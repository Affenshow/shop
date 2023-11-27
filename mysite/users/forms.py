# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from Address.forms import AddressForm
from users.models import User

class UserRegistrationForm(UserCreationForm):
    Address_form = AddressForm()  # Добавим поле для адреса в форму регистрации

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']       

class UserProfileForm(forms.ModelForm):
    Address_form = AddressForm()  # Добавим поле для адреса в форму профиля

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number']



