from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'firstname', 'lastname', 'bio', 'website', 'email', 'github', 'phone', 'address', 'city', 'state', 'zipcode', 'country', 'twitter', 'linkedin', 'facebook', 'instagram', 'youtube']




