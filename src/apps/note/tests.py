from django.test import TestCase
from django.contrib.auth.models import User
from apps.note.models import Note
from django.utils import timezone

class NoteTestCase(TestCase):
    def test_defaults(self):
        """Test Note model default values"""
        
        # Test automatic date in 'created' field
        user = User.objects.create(username='foo', password='foo')
        now = timezone.now()
        note = Note.objects.create(title='foo', content='foo', author=user)
        self.assertEqual(note.created.date(), now.date())
