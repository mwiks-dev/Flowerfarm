from django import forms
from .models import Production, Profile

class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = ['greenhouse_number','variety','length','rejected_flowers','rejection_reason']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']