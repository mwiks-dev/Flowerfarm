from django import forms
from .models import Production

class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = ['greenhouse_number','variety','length','rejected_flowers','rejection_reason']
