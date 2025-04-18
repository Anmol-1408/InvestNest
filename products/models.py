from django.db import models
from accounts.models import Profile
import uuid

# --- Product Model ---
class Product(models.Model):
    developer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        limit_choices_to={'is_developer': True}
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    features = models.TextField(blank=True)
    financial_projection = models.TextField(blank=True)
    icon = models.ImageField(upload_to='images/')
    screenshot = models.ImageField(upload_to='images/screenshots/')
    link = models.URLField()
    pub_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    upvote = models.IntegerField(default=0)
    tags = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    goal = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=10.00  # Default goal value (e.g., $100,000)
    )
    funding = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00  # Default funding value (e.g., $0 initially)
    )

    def summary(self):
        return self.description[:100] + "..." if self.description else ""

    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    def features_list(self):
        return [feature.strip() for feature in self.features.split(',') if feature.strip()]

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %d, %Y')

    def __str__(self):
        return self.title


# --- Investment Model ---
class Investment(models.Model):
    investor = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        limit_choices_to={'is_investor': True}
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    equity = models.DecimalField(max_digits=5, decimal_places=2)  # 100.00 max = 100%
    description = models.TextField()
    message = models.TextField(blank=True, null=True)
    invested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.investor.user.username} invested in {self.product.title}"


# --- Community Discussion Model ---
class CommunityDiscussion(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# --- Community Reply Model ---
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
        return f'Reply by {self.replied_by.user.username} on "{self.discussion.title}"'


# --- Event Model ---
class Event(models.Model):
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_time = models.DateTimeField()
    link = models.URLField(max_length=500, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
