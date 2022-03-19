from django.shortcuts import render
from datetime import datetime

from .models import Product, Picture
from .forms import SaleForm

def home(request):
    clock_products = Product.objects.filter(type= 'clock').filter(finished_date__gt=datetime.now()).order_by('finished_date')[:8]
    dutch_products = Product.objects.filter(type= 'dutch').filter(finished_date__gt=datetime.now()).order_by('finished_date')[:8]
    sealed_products = Product.objects.filter(type= 'sealed').filter(finished_date__gt=datetime.now()).order_by('finished_date')[:8]
    return render(request, 'app/home.html', {'clock_products': clock_products, 'dutch_products': dutch_products, 'sealed_products': sealed_products})

def section(request, type):
    products = Product.objects.filter(type= type).filter(finished_date__gt=datetime.now()).order_by('finished_date')
    return render(request, 'app/section.html', {'products': products})

def product(request, id):
    product = Product.objects.get(id= id)
    return render(request, 'app/product.html', {'product': product})

def sale(request):

    data = {'message': 'Something went wrong'}

    if request.method == 'POST':

        product = SaleForm(data = request.POST)

        if product.is_valid():
            product.instance.seller = request.user #User that is sign in
            if 'final_bid' in request.POST: product.final_bid = request.POST['final_bid']
            product.save()

            """ Save the files on the db """
            for file in request.FILES.getlist("images"):
                picture = Picture()
                picture.product = product.instance
                picture.image = file
                picture.save()

            data['message'] = 'Auction save'
        
    return render(request, 'app/sale.html', data)

def profile(request):
    return render(request, 'app/profile.html', {})