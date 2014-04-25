from django import forms

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