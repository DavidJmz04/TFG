from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib import messages
from datetime import datetime

from .models import Product, Bid, Picture
from .forms import SaleForm, BidForm, UserForm

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from .serializers import BidSerializer

class BidViewset(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    http_method_names = ['get', 'post']

    """ Get all bids """
    """ def list(self, request):
        #raise MethodNotAllowed("GET")#No permitirlo """
    
    """ Get only a bid """
    def retrieve(self, request, pk=None):
        print('Entra')
        return super().retrieve(request)

    """ Post a bid """
    def create(self, request):
        product = Product.objects.get(id= request.data.dict()['product'])

        # Add the bid if it is the first one on dutch auctions and if it is the biggest one on clock auctions
        if (product.type == 'dutch' and product.winner == None) or (product.type == 'clock' and Bid.objects.filter(product = product).filter(price__gte=request.data.dict()['price']).count() == 0):
            product.winner = request.user
            product.save()
            
        # Add the bid on sealed auctions
        elif product.type == 'sealed':
            # Only save the biggest one as the winner
            if Bid.objects.filter(product = product).filter(price__gte=request.data.dict()['price']).count() == 0:
                product.winner = request.user
                product.save()

        else:
            raise ParseError('Someone made a bigger bid')
        
        return super().create(request)

""" Pass 8 products of each type to the view """
def home(request):
    clock_products = Product.objects.filter(type= 'clock').filter(finished_date__gt=datetime.now()).order_by('finished_date')[:5]
    dutch_products = Product.objects.filter(type= 'dutch').filter(finished_date__gt=datetime.now()).filter(winner__isnull=True).order_by('finished_date')[:5]
    sealed_products = Product.objects.filter(type= 'sealed').filter(finished_date__gt=datetime.now()).order_by('finished_date')[:5]
    return render(request, 'app/home.html', {'clock_products': clock_products, 'dutch_products': dutch_products, 'sealed_products': sealed_products})

""" Pass products of its type that are not finished to the view """
def section(request, type):
    if type == 'dutch': products = Product.objects.filter(type= type).filter(finished_date__gt=datetime.now()).filter(winner__isnull=True).order_by('finished_date')
    else: products = Product.objects.filter(type= type).filter(finished_date__gt=datetime.now()).order_by('finished_date')

    return render(request, 'app/section.html', {'products': products})

""" Pass the product and receive the bidForm stored on the db to the view """
def product(request, id):
    product = Product.objects.get(id= id)
    
    """ Save the bid on the db """
    if request.method == 'POST':
        bid = BidForm(data = request.POST)
        if bid.is_valid():
            # Add the bid if it is the first one on dutch auctions and if it is the biggest one on clock auctions
            if (product.type == 'dutch' and product.winner == None) or (product.type == 'clock' and Bid.objects.filter(product = product).filter(price__gte=bid.cleaned_data['price']).count() == 0):
                bid.instance.product = product
                bid.instance.buyer = request.user
                bid.save()

                product.winner = request.user
                product.save()

                messages.success(request, 'Bid successfully created')
            
            # Add the bid on sealed auctions
            elif product.type == 'sealed':
                # only save the biggest one as the winner
                if Bid.objects.filter(product = product).filter(price__gte=bid.cleaned_data['price']).count() == 0:
                    product.winner = request.user
                    product.save()

                bid.instance.product = product
                bid.instance.buyer = request.user
                bid.save()

                messages.success(request, 'Bid successfully created')

            else:
                messages.warning(request,'Someone made a bigger bid')
        else:
            messages.warning(request,'Something went wrong')

    finished = product.finished_date.timestamp() < datetime.now().timestamp()
    if product.type == 'dutch' and product.winner != None: finished = True
    
    return render(request, 'app/product.html', {'product': product, 'finished': finished})

""" Receive the saleForm and the images stored on the db to the view """
def sale(request):
    if request.method == 'POST':
        product = SaleForm(data = request.POST)

        if product.is_valid():
            product.instance.seller = request.user
            if request.POST['final_bid'] < request.POST['initial_bid']:
                product.save()

                """ Save the files on the db """
                for file in request.FILES.getlist("images"):
                    picture = Picture()
                    picture.product = product.instance
                    picture.image = file
                    picture.save()
                
                messages.success(request, 'Sale successfully created')
            else:
                messages.warning(request, 'Minimum price has to be lower than the maximum one')
        else:
            messages.warning(request, 'Something went wrong')

    return render(request, 'app/sale.html')

"""  """
def profile(request):
    q1 = Product.objects.filter(winner= request.user).filter(type='dutch')
    q2 = Product.objects.filter(winner= request.user).filter(type__in=['clock','sealed'], finished_date__lt=datetime.now())
    products= q1.union(q2)

    products_participated = Product.objects.filter(bid__buyer = request.user).distinct()
    sales = Product.objects.filter(seller= request.user)

    # First time on the view
    if request.method != 'POST':
        return render(request, 'app/profile.html', {'form': UserForm(initial={'first_name': request.user.first_name, 'last_name': request.user.last_name, 'username': request.user.username, 'email': request.user.email}), 'products': products, 'products_participated': products_participated, 'sales': sales})
    
    # Editing user
    else:
        userForm = UserForm(data = request.POST)
        if userForm.is_valid():
            if 'image' in request.POST: userForm.instance.profile.image = request.POST['image']
            userForm.save()
            logout(request)
            new_user = authenticate(request, username=userForm.cleaned_data['username'], password=userForm.cleaned_data['password1'])
            login(request, new_user)
            messages.success(request, 'Changes successfully done')
            return render(request, 'app/profile.html', {'form': userForm, 'products': products, 'products_participated': products_participated, 'sales': sales})
        else:
            return render(request, 'app/profile.html', {'oldForm': userForm, 'products': products, 'products_participated': products_participated, 'sales': sales})

""" Receive the login user or the new user to the view """
def login_signin(request):  
    
    # First time on the view
    if request.method != 'POST':
        return render(request, 'app/login.html', {'form': UserForm, 'signin': False})
    
    # Trying to login/signin
    else:
        # Login
        if request.POST.get('password2') is None:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Log in successful')
                return render(request, 'app/home.html')
            else:
                return render(request, 'app/login.html', {'form': UserForm, 'username': request.POST['username'], 'password': request.POST['password'], 'signin': False})
        # Sigin
        else:
            userForm = UserForm(data = request.POST)
            if userForm.is_valid():
                userForm.save()
                new_user = authenticate(request, username=userForm.cleaned_data['username'], password=userForm.cleaned_data['password1'])
                login(request, new_user)
                messages.success(request, 'Sign in successful')
                return render(request, 'app/home.html')
            else:    
                return render(request, 'app/login.html', {'oldForm': userForm, 'signin': True})

""" Logout the user view """
def user_logout(request):
    logout(request)
    messages.success(request, 'Log out successful')
    return render(request, 'app/home.html')