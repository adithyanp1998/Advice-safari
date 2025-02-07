from django import forms
from .models import Product
class Productform(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'phonenumber', 'price', 'category', 'image']