from django import forms
from .models import Production, RejectedData
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
    
class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = ['production_date','greenhouse_number','varieties','total_number','length']

        widgets = {
                    'production_date' : DatePickerInput(),
                    
                }


class RejectedDataForm(forms.ModelForm):
    class Meta:
        model = RejectedData
        fields = ['rejection_date','greenhouse_number','varieties','rejected_number','rejection_reason']

        widgets = {
                    'rejection_date' : DatePickerInput(),
                    
                }
    
