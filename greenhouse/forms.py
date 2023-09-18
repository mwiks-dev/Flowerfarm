from django import forms
from .models import Production, Profile

class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = ['greenhouse_number','variety','length','rejected_flowers','rejection_reason']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Get the 'request' from kwargs
        super(ProductionForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(ProductionForm, self).save(commit=False)
        instance.user = self.request.user  # Set the user field to the current user
        if commit:
            instance.save()
        return instance

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']