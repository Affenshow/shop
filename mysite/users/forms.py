# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'street', 'city', 'country', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['username'].widget.attrs.update({'placeholder': 'Выберите имя пользователя'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Введите ваше имя'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Введите вашу фамилию'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Введите ваш email'})
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'Введите ваш номер телефона'})
        self.fields['street'].widget.attrs.update({'placeholder': 'Введите вашу улицу'})
        self.fields['city'].widget.attrs.update({'placeholder': 'Введите ваш город'})
        self.fields['country'].widget.attrs.update({'placeholder': 'Введите вашу страну'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Введите ваш пароль'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Подтвердите ваш пароль'})

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['username'].widget.attrs.update({'placeholder': 'Введите имя пользователя'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Введите пароль'})

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'readonly': True}))
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'street', 'city', 'country', 'image']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'




