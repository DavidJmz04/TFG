from django.shortcuts import render
from .models import Product, Picture
from .forms import SaleForm

def home(request):
    products = Product.objects.all()
    return render(request, 'app/home.html', {'products': products})

def section(request, type):
    products = Product.objects.filter(type= type).order_by('finished_date')
    return render(request, 'app/section.html', {'products': products})

def product(request):
    return render(request, 'app/product.html', {})

def sale(request):

    data = {'message': 'Something went wrong'}

    if request.method == 'POST':

        product = SaleForm(data = request.POST)

        if product.is_valid():
            product.instance.seller = request.user #User that is sign in
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