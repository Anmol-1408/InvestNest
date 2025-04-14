from django import forms
from django.db.models import fields
from .models import Product, Investment, CommunityDiscussion, CommunityReply, Event


class ProductForm(forms.ModelForm):

	class Meta:
		model = Product
		fields = [
		    'title', 'description', 'features',
		    'financial_projection', 'icon', 'screenshot', 'link', 'pub_date',
		    'tags', 'category', 'is_published', 'is_featured'
		]
		widgets = {
		    'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
		    'description': forms.Textarea(attrs={'rows': 4}),
		    'features': forms.Textarea(attrs={'rows': 2}),
		    'financial_projection': forms.Textarea(attrs={'rows': 2}),
		    'tags':
		    forms.TextInput(attrs={'placeholder': 'Comma-separated tags'}),
		    'category': forms.TextInput(attrs={'placeholder': 'Category'}),
		}


class InvestmentForm(forms.ModelForm):

	class Meta:
		model = Investment
		fields = [
		    'investor', 'product', 'amount', 'equity', 'description', 'message',
		]
		widgets = {
		    'amount': forms.NumberInput(attrs={'step': '0.01'}),
		    'equity': forms.NumberInput(attrs={'step': '0.01'}),
		    'description': forms.Textarea(attrs={'rows': 4}),
		    'message': forms.Textarea(attrs={'rows': 4}),
		}

class CommunityDiscussionForm(forms.ModelForm):
    class Meta:
        model = CommunityDiscussion
        fields = ['title', 'description']

class CommunityReplyForm(forms.ModelForm):
    class Meta:
        model = CommunityReply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your thoughtful reply here...'
            })
        }
        
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date_time']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }