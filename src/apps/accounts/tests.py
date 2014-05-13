from apps.accounts.models import StudentTransfer
from apps.plan.models import Lesson
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

class TransferTestCase(TestCase):
    
    def setUp(self):
        # Load fixtures
        call_command('loaddata', 'plan.yaml', verbosity=0)
        call_command('loaddata', 'settings', verbosity=0)
        call_command('loaddata', 'account', verbosity=0)
        
    def test_proper_transfer(self):
        user1 = User.objects.get(pk=1)
        user1_transfers = StudentTransfer.objects.filter(account=user1.profile)
        self.assertEqual(user1_transfers.count(), 0)

        lesson1 = Lesson.objects.get(pk=6)
        lesson2 = Lesson.objects.get(pk=7)
        
        self.assertIn(lesson1, user1.profile.get_plan())
        self.assertNotIn(lesson2, user1.profile.get_plan())
        
        user1.profile.make_transfer(lesson1, lesson2)
        
        self.assertIn(lesson2, user1.profile.get_plan())
        self.assertNotIn(lesson1, user1.profile.get_plan())
    
    def test_transfer_from_not_attending_lesson(self):
        user1 = User.objects.get(pk=1)
        lesson1 = Lesson.objects.get(pk=1)
        lesson2 = Lesson.objects.get(pk=4)
        
        self.assertNotIn(lesson1, user1.profile.get_plan())
        self.assertNotIn(lesson2, user1.profile.get_plan())
        
        self.assertRaises(Exception, user1.profile.make_transfer, lesson1, lesson2)

        self.assertNotIn(lesson1, user1.profile.get_plan())
        self.assertNotIn(lesson2, user1.profile.get_plan())
    
    def test_transfer_to_a_different_type_of_lesson(self):
        user1 = User.objects.get(pk=1)
        lesson1 = user1.profile.get_plan().filter(type__iexact='CW')[0]
        lesson2 = Lesson.objects.filter(type__iexact='WYK')[0]
        
        self.assertIn(lesson1, user1.profile.get_plan())
        self.assertNotIn(lesson2, user1.profile.get_plan())
        
        self.assertRaises(Exception, user1.profile.make_transfer, lesson1, lesson2)
        
    def test_transfer_destroy(self):
        user1 = User.objects.get(pk=1)
        user1_transfers = StudentTransfer.objects.filter(account=user1.profile)
        self.assertEqual(user1_transfers.count(), 0)

        lesson1 = Lesson.objects.get(pk=6)
        lesson2 = Lesson.objects.get(pk=7)
        
        self.assertIn(lesson1, user1.profile.get_plan())
        self.assertNotIn(lesson2, user1.profile.get_plan())
        
        user1.profile.make_transfer(lesson1, lesson2)
        
        self.assertIn(lesson2, user1.profile.get_plan())
        self.assertNotIn(lesson1, user1.profile.get_plan())
        self.assertTrue(StudentTransfer.objects.filter(target=lesson2, account=user1.profile).exists())
        
        user1.profile.make_transfer(lesson2, lesson1)
        
        self.assertIn(lesson1, user1.profile.get_plan())
        self.assertNotIn(lesson2, user1.profile.get_plan())
        self.assertFalse(StudentTransfer.objects.filter(target=lesson2, account=user1.profile).exists())