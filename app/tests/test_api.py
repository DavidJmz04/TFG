from django.test import TestCase, Client

from django.utils import timezone


class ApiTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    """ Post user """
    def test_user(self):
        response = self.client.post('/api/users/', {'username': 'david', 'password': 'David123456'})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['username'], 'david')
    
    """ Post and get product """
    def test_product(self):
        user = self.client.post('/api/users/', {'username': 'david', 'password': 'David123456'})

        # Unable to post a product if you are not login into the website
        bad_response = self.client.post('/api/products/', {'title': "Test", 'description': "This is a test", 'quantity': 3, 'measure': 'units', 'type': "clock", 'initial_bid': 20, 'origin': "Spain", 'finished_date': timezone.now(), 'seller': user.json()['id']})
        self.assertEqual(bad_response.status_code, 403)
        
        self.client.login(username= 'david', password= 'David123456')

        # Posting two different products
        response_post1 = self.client.post('/api/products/', {'title': "Test1", 'description': "This is a test", 'quantity': 3, 'measure': 'units', 'type': "clock", 'initial_bid': 20, 'origin': "Spain", 'finished_date': timezone.now(), 'seller': user.json()['id']})
        response_post2 = self.client.post('/api/products/', {'title': "Test2", 'description': "This is a test", 'quantity': 3, 'measure': 'units', 'type': "clock", 'initial_bid': 20, 'origin': "Spain", 'finished_date': timezone.now(), 'seller': user.json()['id']})
        self.assertEqual(response_post1.status_code, 201)
        self.assertEqual(response_post2.status_code, 201)
        
        # Getting all the products
        response_get_all = self.client.get('/api/products/')
        self.assertEqual(response_get_all.status_code, 200)
        self.assertEqual(len(response_get_all.json()), 2)
        
        # Getting only one product
        response_get = self.client.get('/api/products/' + str(response_post1.json()['id']) + '/')
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(response_get.json()['title'], 'Test1')
        self.assertEqual(response_get.json()['description'], 'This is a test')
        self.assertEqual(response_get.json()['quantity'], '3.00')
        self.assertEqual(response_get.json()['measure'], 'units')
        self.assertEqual(response_get.json()['type'], 'clock')
        self.assertEqual(response_get.json()['initial_bid'], '20.00')
        self.assertEqual(response_get.json()['origin'], 'Spain')

    """ Post and get higher bid """
    def test_bid(self):
        user = self.client.post('/api/users/', {'username': 'david', 'password': 'David123456'})
        self.client.login(username= 'david', password= 'David123456')
        product_clock = self.client.post('/api/products/', {'title': "Test1", 'description': "This is a test", 'quantity': 3, 'measure': 'units', 'type': "clock", 'initial_bid': 20, 'origin': "Spain", 'finished_date': timezone.now() + timezone.timedelta(hours=1), 'seller': user.json()['id']})
        product_sealed = self.client.post('/api/products/', {'title': "Test2", 'description': "This is a test", 'quantity': 3, 'measure': 'units', 'type': "sealed", 'initial_bid': 20, 'origin': "Spain", 'finished_date': timezone.now() + timezone.timedelta(hours=1), 'seller': user.json()['id']})
        product_dutch = self.client.post('/api/products/', {'title': "Test3", 'description': "This is a test", 'quantity': 3, 'measure': 'units', 'type': "dutch", 'initial_bid': 20, 'final_bid': 5, 'origin': "Spain", 'finished_date': timezone.now() + timezone.timedelta(hours=1), 'seller': user.json()['id']})
        self.client.logout()
        
        # Unable to post a bid if you are not login into the website
        bad_response1 = self.client.post('/api/bids/', {'price': 25, 'product': product_clock.json()['id'], 'buyer': user.json()['id']})
        self.assertEqual(bad_response1.status_code, 403)

        self.client.login(username= 'david', password= 'David123456')

        # Unable to post a bid if is lower than the initial bid
        bad_response2 = self.client.post('/api/bids/', {'price': 10, 'product': product_clock.json()['id'], 'buyer': user.json()['id']})
        self.assertEqual(bad_response2.status_code, 400)

        # Unable to post a bid if is lower than the final bid on dutch auctions
        bad_response3 = self.client.post('/api/bids/', {'price': 2, 'product': product_dutch.json()['id'], 'buyer': user.json()['id']})
        self.assertEqual(bad_response3.status_code, 400)

        # Posting two different bids on clock auctions
        response_post1 = self.client.post('/api/bids/', {'price': 20, 'product': product_clock.json()['id'], 'buyer': user.json()['id']})
        response_post2 = self.client.post('/api/bids/', {'price': 25, 'product': product_clock.json()['id'], 'buyer': user.json()['id']})
        self.assertEqual(response_post1.status_code, 201)
        self.assertEqual(response_post2.status_code, 201)

        # Posting two bids on sealed auctions, you can post a lower bid than the actual
        response_post3 = self.client.post('/api/bids/', {'price': 30, 'product': product_sealed.json()['id'], 'buyer': user.json()['id']})
        response_post4 = self.client.post('/api/bids/', {'price': 20, 'product': product_sealed.json()['id'], 'buyer': user.json()['id']})
        self.assertEqual(response_post3.status_code, 201)
        self.assertEqual(response_post4.status_code, 201)

        # Posting a bid on dutch auctions
        response_post5 = self.client.post('/api/bids/', {'price': 12, 'product': product_dutch.json()['id'], 'buyer': user.json()['id']})
        self.assertEqual(response_post5.status_code, 201)

        # Unable to post a bid if is lower than the actual bid on clock auctions
        bad_response4 = self.client.post('/api/bids/', {'price': 23, 'product': product_clock.json()['id'], 'buyer': user.json()['id']})
        self.assertEqual(bad_response4.status_code, 400)

        # Unable to post a bid if dutch auction is finished (Someone made the first bid)
        bad_response5 = self.client.post('/api/bids/', {'price': 10, 'product': product_clock.json()['id'], 'buyer': user.json()['id']})
        self.assertEqual(bad_response5.status_code, 400)

        # Unable to get the bigger bid on sealed auctions
        bad_response6 = self.client.get('/api/bids/' + str(product_sealed.json()['id']) + '/')
        self.assertEqual(bad_response6.status_code, 400)

        # Getting the higher bid
        response_get = self.client.get('/api/bids/' + str(product_clock.json()['id']) + '/')
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(response_get.json()[0]['price'], '25.00')