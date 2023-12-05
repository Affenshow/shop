# forms.py
from django import forms
from .models import ProductRating

class ProductRatingForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        fields = ['rating']

 
