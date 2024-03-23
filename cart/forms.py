from django import forms
from django.core.exceptions import ValidationError
from . import models


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.CartOrder
        fields = ['fio', 'address', 'phone_number']
        widgets = {
            'fio': forms.TextInput(attrs={
                'class': 'form-group'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-group'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-group'
            })
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if len(phone_number) not in [9, 12]:
            raise ValidationError('Wrong number of digits')
        return phone_number
