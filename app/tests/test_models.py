from django.test import TestCase

from django.contrib.auth.models import User
from app.models import Bid, Product, Profile

from django.utils import timezone


class UserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username= "david")
        user.set_password('David123456')
        user.save()

        Profile.objects.create(stars= 3, user= user)

    def test_user(self):
        user = User.objects.get(username= "david")
        self.assertEqual(user.username, 'david')

    def test_profile(self):
        user = User.objects.get(username= "david")
        self.assertEqual(user.profile.stars, 3)

class ProductTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username= "david")
        user.set_password('David123456')
        user.save()
        product= Product.objects.create(title= "Test", description= "This is a test", quantity= 3, measure= 'units', type="clock", initial_bid= 20, origin= "Spain", finished_date= timezone.now(), seller= user)

        Bid.objects.create(price= 10, product= product, buyer= user)
        Bid.objects.create(price= 20, product= product, buyer= user)

    def test_product(self):
        product = Product.objects.get(title= "Test")
        self.assertEqual(product.title, 'Test')
        self.assertEqual(product.description, 'This is a test')
        self.assertEqual(product.quantity, 3)
        self.assertEqual(product.measure, 'units')
        self.assertEqual(product.type, 'clock')
        self.assertEqual(product.initial_bid, 20)
        self.assertEqual(product.origin, 'Spain')

    def test_bid(self):
        product = Product.objects.get(title= "Test")
        self.assertEqual(product.bid_set.first().price, 10)
        self.assertEqual(product.bid_set.count(), 2)


    