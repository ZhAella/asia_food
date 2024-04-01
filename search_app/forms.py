from django import forms


class SearchForm(forms.Form):
    search = forms.TextInput(attrs={'class': 'form-group'})
