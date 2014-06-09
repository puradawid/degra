# -*- coding: utf-8 -*-

from apps.plan.models import Post
from django import forms
from django.forms.models import ModelForm

## Form for importing students from csv file
#
class ImportCSVForm(forms.Form):
    #semestr = forms.IntegerField(label='Semestr')
    #field_of_study = forms.ChoiceField(label='Kierunek', choices=Group.FIELD_CHOICES)
    file = forms.FileField(label='Plik .csv')
    
    ## Validate if uploaded file have csv format. If not raise ValidationError exception
    #
    # @return Cleander data with validated file extenstion
    # @raise ValidationError if uploaded file is not csv file
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

## Form for add or edit post
#    
class NewsForm(ModelForm):
    class Meta:
        model = Post
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Tytuł'}),
            'content': forms.Textarea(attrs={'placeholder': 'Treść'}),
            }

    


    
    
    
    
    
    
    
    
    
    
    