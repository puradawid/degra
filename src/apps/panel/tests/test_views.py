from django.test import TestCase
from model_mommy import mommy
from django.test.client import Client
from django.core.urlresolvers import reverse

from apps.plan.models import Post

class AddNewsTest(TestCase):

    def setUpClass(self):
        self.post = mommy(Post)

    def setUp(self):
        self.client = Client()    
    
    def creationTest(self):
        self.client.post(reverse("add_news"), {"title" : self.post.title, "content" : self.post.content})
        self.assertTrue(False)
        