# items/forms.py

from django import forms
from .models import Item, Category

class ItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)

    class Meta:
        model = Item
        fields = ['title', 'description', 'price', 'condition', 'video', 'category']