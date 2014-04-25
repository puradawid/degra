from django.test import TestCase
from apps.panel.forms import ImportCSVForm
from django.core.files.uploadedfile import SimpleUploadedFile

class ImportCSVFormTestCase(TestCase):
    def setUp(self):
        pass
    
    def test_invalid_form(self):
        """Submit invalid data"""
        
        # Submit empty form
        form = ImportCSVForm()
        self.assertFalse(form.is_valid())
        