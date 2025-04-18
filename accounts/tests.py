from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile

class UserAuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
    
    def test_login_view_valid_user(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertRedirects(response, reverse('profile'))

    def test_login_view_invalid_user(self):
        response = self.client.post(reverse('login'), {
            'username': 'wronguser',
            'password': 'wrongpass',
        })
        self.assertContains(response, 'Invalid username or password', status_code=200)

    def test_signup_view_creates_user_and_profile(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'strongpass123',
            'password2': 'strongpass123',
        })
        self.assertEqual(User.objects.count(), 2)  # 1 from setUp + 1 new
        new_user = User.objects.get(username='newuser')
        self.assertTrue(Profile.objects.filter(user=new_user).exists())
        self.assertRedirects(response, reverse('profile_setup'))

    def test_profile_setup_view_requires_login(self):
        response = self.client.get(reverse('profile_setup'))
        self.assertRedirects(response, '/accounts/login/?next=/profile_setup/')  # Default login redirect

    def test_profile_view_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, '/accounts/login/?next=/profile/')

    def test_profile_created_on_user_creation(self):
        user = User.objects.create_user(username='profileuser', password='abc123')
        self.assertTrue(Profile.objects.filter(user=user).exists())

