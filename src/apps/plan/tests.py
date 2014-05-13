from django.core.management import call_command
from django.test import TestCase

class PlanTestCase(TestCase):
    
    def setUp(self):
        # Load fixtures
        call_command('loaddata', 'account', verbosity=0)
        call_command('loaddata', 'plan', verbosity=0)
        call_command('loaddata', 'usertolesson', verbosity=0)