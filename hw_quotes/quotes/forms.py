from django.forms import ModelForm, CharField, TextInput, SelectMultiple
from .models import Author, Quote, Tag
from django import forms


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]
        widgets = {
            'fullname': TextInput(attrs={"class": "form-control"}),
            'born_date': TextInput(attrs={"class": "form-control"}),
            'born_location': TextInput(attrs={"class": "form-control"}),
            'description': TextInput(attrs={"class": "form-control"}),
        }


class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        fields = ["quote", "tags", "author"]
        widgets = {
            'quote': TextInput(attrs={"class": "form-control"}),
            'tags': SelectMultiple(attrs={"class": "form-control"}),
        }
