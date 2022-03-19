from distutils.command.upload import upload
from django.conf import settings
from django.db import models
from django.utils import timezone

""" 
Represents each product on the db 
"""
class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(max_length=30)
    initial_bid = models.DecimalField(max_digits=8, decimal_places=2) #Para subastas ascendentes y a ciegas es el precio suelo, para subastas descendentes es el precio máximo
    final_bid = models.DecimalField(max_digits=8, decimal_places=2, default=0) #Para subastas descendentes es el precio suelo
    origin = models.CharField(max_length=30)
    created_date = models.DateTimeField(default=timezone.now) #Para subastas descendentes nos permite modificar la bajada de precio
    finished_date = models.DateTimeField() #Para subastas ascendentes y a ciegas se acaba, para subastas descendentes es el tiempo que tarda en ponerse al minimo

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

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

    """ def __str__(self):
        return self.product """


""" 
Represents each product picture on the db 
"""
class Picture(models.Model):
    image = models.ImageField(upload_to='products')

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    """ def __str__(self):
        return self.product """
