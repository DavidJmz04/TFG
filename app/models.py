from django.conf import settings
from django.db import models
from django.utils import timezone

""" 
Represents each product on the db 
"""
class Product(models.Model):
    title = models.CharField(max_length=200)
    info = models.TextField()
    type = models.CharField(max_length=30)
    finished_date = models.DateTimeField() #Para subastas ascendentes y a ciegas se acaba, para subastas descendentes es el tiempo que tarda en ponerse al minimo

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

""" 
Represents each bid on the db 
"""
class Bid(models.Model):
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    created_date = models.DateTimeField(default=timezone.now)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    #TODO: Devolver el comprador
    """ def __str__(self):
        return self.buyer """


""" 
Represents each picture on the db 
"""
class Picture(models.Model):
    image = models.ImageField() #TODO: Guardarla en algún lado

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    #TODO: Devolver el producto
    """ def __str__(self):
        return self.buyer """
