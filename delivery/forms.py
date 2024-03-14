from django import forms
from . import models


class FoodForm(forms.ModelForm):
    class Meta:
        model = models.Food
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-group'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-group'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-group'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-group'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-group'
            })
        }


class DrinkForm(forms.ModelForm):
    class Meta:
        model = models.Drink
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-group'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-group'
            }),
            'volume': forms.NumberInput(attrs={
                'class': 'form-group'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-group'
            })
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
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
