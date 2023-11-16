from django import forms
from .models import Production, RejectedData

class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = ['greenhouse_number','varieties','total_number','length']

class RejectedDataForm(forms.ModelForm):
    class Meta:
        model = RejectedData
        fields = ['greenhouse_number','varieties','rejected_number','rejection_reason']

    
