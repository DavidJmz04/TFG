from dataclasses import fields
from django import forms
from .models import Product

class SaleForm (forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'type', 'initial_bid', 'origin', 'finished_date']