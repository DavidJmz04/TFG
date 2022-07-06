from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver

from django.utils import timezone

from django.contrib.auth.models import User
from app.models import Product

class RegisterTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test0_register(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login'))
        self.selenium.execute_script("arguments[0].click();", self.selenium.find_element_by_xpath('//a[text()="Sign in"]'))

        self.selenium.find_element_by_id('id_first_name').send_keys('Name')
        self.selenium.find_element_by_id('id_last_name').send_keys('Last Name')
        self.selenium.find_element_by_id('id_username').send_keys('username')
        self.selenium.find_element_by_id('id_email').send_keys('mail@gmail.com')
        self.selenium.find_element_by_id('id_password1').send_keys('tesT123456')
        self.selenium.find_element_by_id('id_password2').send_keys('tesT123456')

        self.selenium.find_element_by_xpath('//button[text()="Sign in"]').click()

        user = User.objects.get(username= "username")
        self.assertEqual(user.username, 'username')
        self.assertEqual(user.first_name, 'Name')
        self.assertEqual(user.last_name, 'Last Name')
        self.assertEqual(user.email, 'mail@gmail.com')

class SeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        user = User.objects.create(username= "test")
        user.set_password('Test123456')
        user.save()

        self.selenium.get('%s%s' % (self.live_server_url, '/login'))
        self.selenium.find_element_by_id('username').send_keys('test')
        self.selenium.find_element_by_id('password').send_keys('Test123456')
        self.selenium.find_element_by_xpath('//button[text()="Log in"]').click()

        Product.objects.create(title= "Test1", description= "This is a test", quantity= 3, measure= 'units', type="clock", initial_bid= 20, origin= "Spain", finished_date= timezone.now() + timezone.timedelta(hours=1), seller= user)
        Product.objects.create(title= "Test2", description= "This is a test", quantity= 3, measure= 'units', type="dutch", initial_bid= 20, origin= "Spain", finished_date= timezone.now() + timezone.timedelta(hours=1), seller= user)
        Product.objects.create(title= "Test3", description= "This is a test", quantity= 3, measure= 'units', type="sealed", initial_bid= 20, origin= "Spain", finished_date= timezone.now() + timezone.timedelta(hours=1), seller= user)

    def test0_navbar(self):
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        self.assertEqual(self.selenium.current_url, self.live_server_url + '/')
        self.selenium.execute_script("arguments[0].click();", self.selenium.find_element_by_xpath('//a[text()="Clock auctions"]'))
        self.assertEqual(self.selenium.current_url, self.live_server_url + '/section/clock')
        self.selenium.execute_script("arguments[0].click();", self.selenium.find_element_by_xpath('//a[text()="Dutch auctions"]'))
        self.assertEqual(self.selenium.current_url, self.live_server_url + '/section/dutch')
        self.selenium.execute_script("arguments[0].click();", self.selenium.find_element_by_xpath('//a[text()="Sealed bid auctions"]'))
        self.assertEqual(self.selenium.current_url, self.live_server_url + '/section/sealed')

        self.selenium.execute_script("arguments[0].click();", self.selenium.find_element_by_xpath('//a[text()="Sale"]'))
        self.assertEqual(self.selenium.current_url, self.live_server_url + '/sale/')

    def test1_clock_bid(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/section/clock'))
        self.selenium.execute_script("arguments[0].click();", self.selenium.find_element_by_class_name('row').find_element_by_tag_name('a'))
        
        self.selenium.find_element_by_xpath('//button[text()="Pay"]').click()
        
        product = Product.objects.get(title= "Test1")
        self.assertEqual(product.bid_set.first().price, 20)

    def test2_dutch_bid(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/section/dutch'))
        self.selenium.execute_script("arguments[0].click();", self.selenium.find_element_by_class_name('row').find_element_by_tag_name('a'))
        
        self.selenium.find_element_by_xpath('//button[text()="Pay"]').click()
        product = Product.objects.get(title= "Test2")
        self.assertEqual(product.bid_set.first().price, 60)

    def test3_sealed_bid(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/section/sealed'))
        self.selenium.execute_script("arguments[0].click();", self.selenium.find_element_by_class_name('row').find_element_by_tag_name('a'))
        
        self.selenium.find_element_by_xpath('//button[text()="Pay"]').click()
        
        product = Product.objects.get(title= "Test3")
        self.assertEqual(product.bid_set.first().price, 20)