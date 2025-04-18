from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to='profile/images/', blank=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    
    is_developer = models.BooleanField(default=False)
    is_investor = models.BooleanField(default=False)

    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField()

    # Contact info
    phone = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    # Socials
    github = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

# Automatically create or update user profile
@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
