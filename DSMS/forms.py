from django import forms
from django.forms import ModelForm
from .models import Product

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_quantity', 'category', 'brand']