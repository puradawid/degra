# -*- coding: utf-8 -*-

from django import forms
from django.forms.models import ModelForm
from apps.plan.models import Group, Post

class ImportCSVForm(forms.Form):
    file = forms.FileField(label='Plik .csv')
    
    def clean(self, *args, **kwargs):
        """
            Expand clean method on validate file extension
        """
        cleaned_data = super(ImportCSVForm, self).clean(*args, **kwargs)
        if cleaned_data:
            filename = cleaned_data.get('file').name
            if filename.endswith('.csv') == False:
                raise forms.ValidationError("Nieprawidlowy format pliku")
        
        return cleaned_data
    
class NewsForm(ModelForm):
    class Meta:
        model = Post
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Tytuł'}),
            'content': forms.Textarea(attrs={'placeholder': 'Treść'}),
            }
        
class NewsFormEdit(NewsForm):
    def __init__(self, *args, **kwargs):
        super(NewsFormEdit, self).__init__(*args, **kwargs)
    
        

    


    
    
    
    
    
    
    
    
    
    
    