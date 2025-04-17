from django.db import models
from accounts.models import Profile
import uuid

# Product listings
class Product(models.Model):
    developer = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE,
        limit_choices_to={'is_developer': True}
    )
    title = models.CharField(blank=False, max_length=200)
    description = models.TextField(blank=False)
    features = models.TextField()
    upvote = models.IntegerField(default=0)
    financial_projection = models.TextField()
    icon = models.ImageField(blank=False, upload_to='images/')
    screenshot = models.ImageField(blank=False, upload_to='images/screenshots/')
    link = models.URLField(blank=False)
    pub_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    def summary(self):
        return self.description[:100] + "..."  # Fixed attribute name
    
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def features_list(self):
        return [features.strip() for features in self.features.split(',') if features.strip()]

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

    def __str__(self):
        return self.title


# Investment options
class Investment(models.Model):
    investor = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        limit_choices_to={'is_investor': True}
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    equity = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=False)
    message = models.TextField(blank=True, null=True)
    invested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.investor.user.username} invested in {self.product.title}"


# Community Discussion
class CommunityDiscussion(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CommunityReply(models.Model):
    discussion = models.ForeignKey(
        CommunityDiscussion,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    replied_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reply by {self.replied_by.user.username}'


# Event model for live pitching sessions
class Event(models.Model):
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_time = models.DateTimeField()
    link = models.URLField(max_length=500, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
