from django.shortcuts import render

def home(request):
    return render(request, 'app/home.html', {})

def section(request):
    return render(request, 'app/section.html', {})

def product(request):
    return render(request, 'app/product.html', {})

def sale(request):
    return render(request, 'app/sale.html', {})

def profile(request):
    return render(request, 'app/profile.html', {})