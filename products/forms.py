# forms.py
from django import forms
from .models import Product, Investment, CommunityDiscussion, CommunityReply, Event

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['developer']  # Exclude developer field (set it in the view)
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'features': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Comma-separated Features'}),
            'financial_projection': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Your Valuation'}),
            'link': forms.TextInput(attrs={'placeholder': 'Website link'}),
            'tags': forms.TextInput(attrs={'placeholder': 'Comma-separated tags'}),
            'category': forms.TextInput(attrs={'placeholder': 'Category'}),
        }

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        exclude = ['investor']  # Hide investor field
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'equity': forms.NumberInput(attrs={'step': '0.01'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Optional message for the developer'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(is_published=True)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'product' in self.initial:
            self.fields['product'].initial = self.initial['product']

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Investment amount must be greater than 0.")
        return amount

    def clean_equity(self):
        equity = self.cleaned_data['equity']
        if not (0 < equity <= 100):
            raise forms.ValidationError("Equity must be between 0 and 100%.")
        return equity

class CommunityDiscussionForm(forms.ModelForm):
    class Meta:
        model = CommunityDiscussion
        fields = ['title', 'description']

class CommunityReplyForm(forms.ModelForm):
    class Meta:
        model = CommunityReply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Write your thoughtful reply here...'})
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date_time']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
