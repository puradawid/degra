from model_mommy import mommy
from django_webtest import WebTest

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from apps.plan.models import Post, Group
from apps.accounts.models import Account


class AddNewsTest(TestCase):

    def setUpClass(self):
        self.post = mommy(Post)

    def setUp(self):
        self.client = Client()    
    
    def creationTest(self):
        self.client.post(reverse("add_news"), {"title" : self.post.title, "content" : self.post.content})
        self.assertTrue(False)

class ImportStudentViewTestCase(WebTest):

    def test_import_proper_file(self):
        view = self.app.get(reverse('import_students'))
        form = view.form
        content = "88040,PS3\n88041,PS3\n88042,Ps3"
        form['file'] = "students.csv", content
        response = form.submit().follow()

        self.assertNotContains(response, "Nieprawidlowy format pliku")
        self.assertContains(response, "Zaimportowano!")
        
        self.assertEqual(Account.objects.filter(index_number__in=("88040", "88041", "88042")).count(), 3)
        self.assertTrue(Group.objects.filter(name="PS3").exists())
        
        self.assertEqual(Group.objects.filter(name__iexact="PS3").count(), 1)

    def test_import_bad_file(self):
        view = self.app.get(reverse('import_students'))
        form = view.form
        content = "88040,PS3\n88041,5PS3\n88042,PS3"
        form['file'] = "students.csv", content

        response = form.submit().follow()

        self.assertNotContains(response, "Nieprawidlowy format pliku")
        self.assertContains(response, "Operacja przerwana!")
        
        self.assertEqual(Account.objects.all().count(), 0)
        self.assertFalse(Group.objects.filter(name="PS3").exists())

    def test_import_two_lists_students(self):
        view = self.app.get(reverse('import_students'))
        form = view.form
        content = "88040,PS3\n88041,PS3\n88042,PS3"
        form['file'] = "students.csv", content
        response = form.submit().follow()

        self.assertNotContains(response, "Nieprawidlowy format pliku")
        self.assertContains(response, "Zaimportowano!")
        
        form = response.form
        
        content = "88040,PS3\n88041,PS3\n88042,PS2"
        form['file'] = "students.csv", content
        response = form.submit().follow()
        
        self.assertEqual(Account.objects.all().count(), 3)
        self.assertTrue(Group.objects.filter(name="PS2").exists())
        self.assertTrue(Account.objects.get(pk="88042").groups.filter(name="PS2").exists())
        self.assertFalse(Account.objects.get(pk="88042").groups.filter(name="PS3").exists())
        self.assertTrue(Group.objects.filter(name="PS3").exists())
        