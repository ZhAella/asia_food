from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from . import models


class CustomerUserForm(UserCreationForm):
    class Meta:
        model = models.CustomerUser
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-group'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-group'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-group'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-group'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-group'
            })
        }


class FoodForm(forms.ModelForm):
    type = forms.ModelChoiceField(queryset=models.FoodType.objects.all(),
                                  widget=forms.Select(attrs={
                                      'class': 'form-group'
                                  }))
    new_food_type = forms.CharField(max_length=100, required=False)

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

    def __init__(self, *args, **kwargs):
        super(FoodForm, self).__init__(*args, **kwargs)
        self.fields['type'].required = False
        self.fields = {
            'name': self.fields['name'],
            'price': self.fields['price'],
            'weight': self.fields['weight'],
            'type': self.fields['type'],
            'new_food_type': self.fields['new_food_type'],
            'photo': self.fields['photo'],
            'description': self.fields['description'],
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

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if len(phone_number) not in [9, 12]:
            raise ValidationError('Wrong number of digits')
        return phone_number
