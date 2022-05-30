from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from datetime import datetime
from decimal import Decimal

from .models import Product, Bid, Picture, Profile
from django.contrib.auth.models import User
from .forms import SaleForm, BidForm, UserForm

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from .serializers import BidSerializer, UserSerializer, ProductSerializer

""" Api view for the users """
class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post']

""" Api view for the bids """
class BidViewset(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post']

    """ Post a bid """
    def create(self, request):
        product = Product.objects.get(id= request.data['product'])

        if product.finished_date.timestamp() > datetime.now().timestamp():
            # Add the bid if it is the first one on dutch auctions and if it is the biggest one on clock auctions
            if (product.type == 'dutch' and product.winner == None and Decimal(request.data['price']) >= product.final_bid) or (product.type == 'clock' and Bid.objects.filter(product = product).filter(price__gte=request.data['price']).count() == 0 and product.initial_bid <= Decimal(request.data['price'])):
                product.winner = User.objects.get(id= request.data['buyer'])
                product.save()
                
            # Add the bid on sealed auctions
            elif product.type == 'sealed' and product.initial_bid <= Decimal(request.data['price']):
                # Only save the biggest one as the winner
                if Bid.objects.filter(product = product).filter(price__gte=request.data['price']).count() == 0:
                    product.winner = User.objects.get(id= request.data['buyer'])
                    product.save()

            else:
                raise ParseError('Someone made a bigger bid')
            
            return super().create(request)
        
        raise ParseError('The auction has been finished')

    """ Get the bigger bid of a product """
    @action(detail=False, url_path='(?P<product>[^/.]+)')
    def bigger_bid(self, request, product):
        p = Product.objects.get(id= product)
        
        if p.type == 'sealed':
            raise ParseError('You cannot know the biggest bid on sealed bid auctions')

        bid = Bid.objects.filter(product= product).order_by('price').reverse()[:1]
        self.queryset = bid
        return super().list(request)

""" Api view for the users """
class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']

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
            # Only allow bidding bigger than the minimum
            if product.type != 'dutch' and bid.instance.price < product.initial_bid: bid.instance.price = product.initial_bid

            # Add the bid if it is the first one on dutch auctions and if it is the biggest one on clock auctions
            if (product.type == 'dutch' and product.winner == None) or (product.type == 'clock' and Bid.objects.filter(product = product).filter(price__gte=bid.cleaned_data['price']).count() == 0):
                
                if product.type == 'dutch' and bid.cleaned_data['price'] > product.final_bid:
                    bid.instance.price = round(product.initial_bid - (((product.initial_bid - product.final_bid) * Decimal(100 - (((product.finished_date.timestamp() - datetime.now().timestamp() - 7200) * 100) / (product.finished_date.timestamp() - product.created_date.timestamp())))) / 100),2)

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
@login_required(login_url='login')
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
@login_required(login_url='login')
def profile(request):
    q1 = Product.objects.filter(winner= request.user).filter(type='dutch')
    q2 = Product.objects.filter(winner= request.user).filter(type__in=['clock','sealed'], finished_date__lt=datetime.now())
    products = q1.union(q2)
    min_products = products.count() if products.count() < 6 else 6

    products_participated = Product.objects.filter(bid__buyer = request.user).distinct()
    min_participated = products_participated.count() if products_participated.count() < 6 else 6

    sales = Product.objects.filter(seller= request.user)
    min_sales = sales.count() if sales.count() < 6 else 6


    # First time on the view
    if request.method != 'POST':
        return render(request, 'app/profile.html', {'form': UserForm(initial={'first_name': request.user.first_name, 'last_name': request.user.last_name, 'username': request.user.username, 'email': request.user.email}), 'products': products, 'min_products': min_products,  'products_participated': products_participated, 'min_participated': min_participated, 'sales': sales, 'min_sales': min_sales, 'edit': False})
    
    # Editing user
    else:
        user = UserForm(data = request.POST, instance = request.user)
        if user.is_valid():
            
            user.save()

            if 'image' in request.FILES:
                if Profile.objects.filter(user= user.instance):
                    profile = Profile.objects.get(user= user.instance)
                    profile.image = request.FILES['image']
                    profile.save()
                else:
                    profile = Profile()
                    profile.user = user.instance
                    profile.image = request.FILES['image']
                    profile.save()

            logout(request)
            new_user = authenticate(request, username=user.cleaned_data['username'], password=user.cleaned_data['password1'])
            login(request, new_user)

            messages.success(request, 'Changes successfully done')

            return render(request, 'app/profile.html', {'form': user, 'products': products, 'min_products': min_products,  'products_participated': products_participated, 'min_participated': min_participated, 'sales': sales, 'min_sales': min_sales, 'edit': False})
        else:
            return render(request, 'app/profile.html', {'oldForm': user, 'products': products, 'min_products': min_products,  'products_participated': products_participated, 'min_participated': min_participated, 'sales': sales, 'min_sales': min_sales, 'edit': True})

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