from django.test import TestCase
from django.urls import reverse
from faker import Faker
from django.contrib.auth.models import User

class LoginTests(TestCase):
    def setUp(self):
        """Create a user with random username and password using Faker"""
        fake = Faker()
        self.username = fake.user_name()
        self.password = fake.password()
        self.user = User.objects.create_user(username=self.username,password=self.password)

    def test_login_page_loads(self):
        """to test the login page to load correctly"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_successful_login(self):
        """To test whether the login works with valid credentials"""  
        response = self.client.post(reverse('login'),{'username':self.username,'password':self.password})  
        self.assertRedirects(response, reverse('todo_list'))

