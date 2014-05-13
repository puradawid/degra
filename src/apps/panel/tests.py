from apps.accounts.models import Account
from apps.panel.forms import ImportCSVForm
from apps.plan.modeldir.group import Group
from django.core.urlresolvers import reverse
from django.test import TestCase
from django_webtest import WebTest

class ImportCSVFormTestCase(TestCase):
    def setUp(self):
        pass
    
    def test_invalid_form(self):
        """Submit invalid data"""
        
        # Submit empty form
        form = ImportCSVForm()
        self.assertFalse(form.is_valid())

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