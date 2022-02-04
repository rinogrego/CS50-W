from django import forms
from django.forms import ModelForm
from .models import *

class ListingForm(ModelForm):
  class Meta:
    model = Listing
    fields = ['title', 'image', 'category', 'description', 'price', 'date_end']
    widgets = {
      'user': forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}),
      'title': forms.TextInput(attrs={'class': 'form-control'}),
      'image': forms.FileInput(attrs={'class': 'form-control-file'}),
      'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category'}),
      'description': forms.Textarea(attrs={'class': 'form-control'}),
      'price': forms.TextInput(attrs={'class': 'form-control'}),
      'date_end': forms.TextInput(attrs={'class': 'form-control'}),
    }
    labels = {
      'title': 'Title',
      'image': 'Listing Image',
      'category': "Category",
      'description': "Description",
      'price': "Starting Price",
      'date_end': "Date Closed",
    }

class CommentListing(ModelForm):
  class Meta:
    model = ListingComment
    fields = ['comment']
    widgets = {
      'user': forms.TextInput(attrs={'class': 'form-control'}),
      'title': forms.TextInput(attrs={'class': 'form-control'}),
      'comment': forms.Textarea(attrs={'class': 'form-control'}),
    }
    

class BiddingForm(ModelForm):
  class Meta:
    model = Bid
    fields = ['price']
    widgets = {
      'user': forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}),
      'price': forms.TextInput(attrs={'class': 'form-control'})
    }
    labels = {
      'price': "Your New Bid"
    }