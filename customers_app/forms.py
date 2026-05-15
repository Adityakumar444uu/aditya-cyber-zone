
from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application

        fields = [
            'customer',
            'application_name',
            'application_no',
            'application_date',
            'status',
            'delivery_date',
            'remarks'
        ]

        widgets = {
            'application_date': forms.DateInput(attrs={'type': 'date'}),
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }
