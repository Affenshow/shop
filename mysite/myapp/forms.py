# forms.py
from django import forms
from .models import ProductRating, Order, Feedback, Review

class ProductRatingForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        fields = ['rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),

        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['total_price']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']
        widgets = {
            'name':    forms.TextInput(attrs={'class':'form-control','placeholder':'Ваше имя'}),
            'email':   forms.EmailInput(attrs={'class':'form-control','placeholder':'Ваш email'}),
            'message': forms.Textarea(attrs={'class':'form-control','rows':4,'placeholder':'Ваше сообщение'}),
        }
        labels = {
            'name':    'Имя',
            'email':   'Email',
            'message': 'Сообщение',
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating':  forms.Select(attrs={
                'class': 'form-control w-auto d-inline-block'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ваш отзыв…'
            }),
        }
        labels = {
            'rating':  'Оценка',
            'comment': 'Комментарий',
        }