# forms.py
from django import forms
from .models import ProductRating, Order

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


 
