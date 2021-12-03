from django import forms
from django.db import models
from django.db.models import fields
from .models import Item

class ItemUpdateForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('name', "crawl")