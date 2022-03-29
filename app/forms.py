from django import forms
from .models import Product, Bid
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SaleForm (forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'type', 'initial_bid', 'origin', 'finished_date']

class BidForm (forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['price']

class UserForm (UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

