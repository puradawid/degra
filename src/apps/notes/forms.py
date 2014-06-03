from apps.notes.models import Note
from django.forms.models import ModelForm
from django import forms

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields=['content']
        
    lesson = forms.CharField(widget=forms.HiddenInput())