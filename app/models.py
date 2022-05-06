from django.conf import settings
from django.db import models
from django.utils import timezone

""" 
Represents each product on the db 
"""
class Product(models.Model):
    MEASURES = (
        ('units', 'Units'),
        ('kg', 'Kilograms'),
        ('l', 'Liters'),
    )

    TYPES = (
        ('clock', 'Clock auctions'),
        ('dutch', 'Dutch auctions'),
        ('sealed', 'Sealed bid auctions'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    measure = type = models.CharField(max_length=30, choices=MEASURES)
    type = models.CharField(max_length=30, choices=TYPES)
    initial_bid = models.DecimalField(max_digits=8, decimal_places=2)
    final_bid = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    origin = models.CharField(max_length=30)
    created_date = models.DateTimeField(default=timezone.now)
    finished_date = models.DateTimeField()

    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='winner', blank=True, null=True)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller')

    def __str__(self):
        return self.title

""" 
Represents each bid on the db 
"""
class Bid(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_date = models.DateTimeField(default=timezone.now)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

""" 
Represents each product picture on the db 
"""
class Picture(models.Model):
    image = models.ImageField(upload_to='products')

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

""" 
Add specific data to the user
"""
class Profile(models.Model):
    stars = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    image = models.ImageField(upload_to='profiles', blank=True, null=True)
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)