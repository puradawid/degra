from django.core.management import call_command
from django.test import TestCase
from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from apps.accounts.models import Account

class TransferViewTestCase(WebTest):

    def setUp(self):
        # Load fixtures
        call_command('loaddata', 'plan.yaml', verbosity=0)
        call_command('loaddata', 'settings', verbosity=0)
        call_command('loaddata', 'account', verbosity=0)

    def test_proper_transfer(self):
        view = self.app.get(reverse('lesson_transfer', kwargs={'pk' : '6'}), user="wi0000")
        form = view.forms[0]
        form['new_lesson'] = '7'

        response = form.submit().follow()

        self.assertNotContains(response, "alert-danger")

        self.assertTrue(Account.objects.get(pk="0000").get_plan().filter(pk=7).exists())
        self.assertFalse(Account.objects.get(pk="0000").get_plan().filter(pk=6).exists())
        
    def test_bad_transfer(self):
        view = self.app.get(reverse('lesson_transfer', kwargs={'pk' : '6'}), user="wi0000")
        form = view.forms[0]
        form['new_lesson'] = '1'
        
        response = form.submit()
        
        self.assertContains(response, "alert-danger")
        
        self.assertTrue(Account.objects.get(pk="0000").get_plan().filter(pk=6).exists())
        self.assertFalse(Account.objects.get(pk="0000").get_plan().filter(pk=1).exists())