from django import forms

class ImportCSVForm(forms.Form):
    file = forms.FileField()