from django.test import TestCase
from apps.post.models import Post
from django.utils import timezone

class PostTestCase(TestCase):
    def test_defaults(self):
        """Test Post model default values"""
        
        # Test automatic date in 'created' field
        now = timezone.now()
        post = Post.objects.create(title='foo', content='foo')
        self.assertEqual(post.created.date(), now.date())
