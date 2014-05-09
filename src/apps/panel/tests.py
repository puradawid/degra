from django.test import TestCase
from apps.panel.forms import ImportCSVForm, NewsForm
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
import os.path
from django.contrib.auth.models import User

class ImportCSVFormTestCase(TestCase):
    def setUp(self):
        pass
    
    def test_invalid_form(self):
        """Submit invalid data"""
        
        # Submit empty form
        form = ImportCSVForm()
        self.assertFalse(form.is_valid())
        
class NewsFormTestCase(TestCase):
    user = None
    
    def setUp(self):
        self.user = User.objects.create(username='wi00000', password='superhardpassword')
        
    def test_invalid_data(self):
        """Submit invalid data"""
        
        # Submit empty form
        form = NewsForm()
        self.assertFalse(form.is_valid())
        
        # Submit too long title
        too_long_title = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        data = { 'title': too_long_title, 'content': 'asdf', 'autor': self.user }
        form = NewsForm(data)
        self.assertFalse(form.is_valid())
        
    def test_valid_data(self):
        """Submit valid data"""
        
        # Submit valid data
        data = { 'title': 'title', 'content': 'content', 'author': self.user }
        form = NewsForm(data)
        self.assertTrue(form.is_valid())
        
class PanelViewTest(TestCase):
    
    def test_not_authorized(self):
        """
            Test view with no user
        """
        
        # This should return 302 code (temporary redirect) TODO: check redirect address
        response = self.client.get('/panel/')
        self.assertEqual(response.status_code, 302)
        
        