from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# User profiles for Developers and Investors
class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	profile_pic = models.ImageField(blank=True, upload_to='profile/images/')
	firstname = models.CharField(max_length=100)
	lastname = models.CharField(max_length=100)
	is_developer = models.BooleanField(default=False)
	is_investor = models.BooleanField(default=False)
	bio = models.TextField(blank=True)
	website = models.URLField(blank=True)
	email = models.EmailField()
	github = models.URLField(blank=True)
	phone = models.CharField(max_length=100, blank=True)
	address = models.CharField(max_length=100, blank=True)
	city = models.CharField(max_length=100, blank=True)
	state = models.CharField(max_length=100, blank=True)
	zipcode = models.CharField(max_length=100, blank=True)
	country = models.CharField(max_length=100, blank=True)
	twitter = models.URLField(blank=True)
	linkedin = models.URLField(blank=True)
	facebook = models.URLField(blank=True)
	instagram = models.URLField(blank=True)
	youtube = models.URLField(blank=True)

	def __str__(self):
		return self.user.username
	
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

	
			
