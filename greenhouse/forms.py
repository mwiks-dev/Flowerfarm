from django import forms
from .models import Production

class ProductionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super(ProductionForm, self).__init__(*args, **kwargs)

        self.user = user

    def save(self, commit=True):
        instance = super(ProductionForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance
    
    class Meta:
        model = Production
        fields = ['greenhouse_number','variety','length','rejected_flowers','rejection_reason']
