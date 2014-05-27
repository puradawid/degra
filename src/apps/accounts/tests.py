from model_mommy import mommy

from apps.accounts.models import Account, StudentTransfer
from apps.plan.models import Lesson
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from apps.plan.modeldir.group import Group
from django.core.exceptions import ValidationError

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
        
    def test_transfer_from_not_attended_lesson(self):
        user1 = User.objects.get(pk=1)
        lesson1 = Lesson.objects.get(pk=7)
        lesson2 = Lesson.objects.get(pk=8)
        
        self.assertNotIn(lesson1, user1.profile.get_plan())
        self.assertNotIn(lesson2, user1.profile.get_plan())
        
        self.assertRaises(Exception, user1.profile.make_transfer, lesson1, lesson2)
        
    def test_transfer_to_different_lesson_type(self):
        user1 = User.objects.get(pk=1)
        lesson1 = Lesson.objects.get(pk=2) # CW
        lesson2 = Lesson.objects.get(pk=1) # PS
        
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
        
    def test_transfer_and_group_change(self):
        user1 = User.objects.get(pk=1)
        lesson1 = Lesson.objects.get(pk=6) # attending, g6
        lesson2 = Lesson.objects.get(pk=7) # g7
        lesson3 = Lesson.objects.get(pk=8) # g8
        old_group = Group.objects.get(pk=6) # attending
        new_group = Group.objects.get(pk=7)
        
        user1.profile.make_transfer(lesson1, lesson2)
        
        self.assertIn(lesson2, user1.profile.get_plan())
        self.assertNotIn(lesson1, user1.profile.get_plan())
        self.assertTrue(StudentTransfer.objects.filter(origin=lesson1, target=lesson2, account=user1.profile).exists())
        
        self.assertIn(old_group, user1.profile.groups.all())
        self.assertNotIn(new_group, user1.profile.groups.all())

        user1.profile.update_group(new_group)
        
        self.assertIn(new_group, user1.profile.groups.all())
        self.assertNotIn(old_group, user1.profile.groups.all())
        # there shouldnt be transfer anymore
        self.assertFalse(StudentTransfer.objects.filter(origin=lesson1, target=lesson2, account=user1.profile).exists())
        
        self.assertRaises(Exception, user1.profile.make_transfer, lesson1, lesson3)
        
    def test_transfer_twice(self):
        user1 = User.objects.get(pk=1)
        lesson1 = Lesson.objects.get(pk=6) # attending, g6
        lesson2 = Lesson.objects.get(pk=4) # g7
        lesson3 = Lesson.objects.get(pk=7) # g8
        
        user1.profile.make_transfer(lesson1, lesson2)
        
        self.assertIn(lesson2, user1.profile.get_plan())
        self.assertNotIn(lesson1, user1.profile.get_plan())
        self.assertNotIn(lesson3, user1.profile.get_plan())
        self.assertTrue(StudentTransfer.objects.filter(origin=lesson1, target=lesson2, account=user1.profile).exists())
        
        user1.profile.make_transfer(lesson2, lesson3)
        
        self.assertIn(lesson3, user1.profile.get_plan())
        self.assertNotIn(lesson1, user1.profile.get_plan())
        self.assertNotIn(lesson2, user1.profile.get_plan())
        self.assertTrue(StudentTransfer.objects.filter(origin=lesson1, target=lesson3, account=user1.profile).count(), 1)
        self.assertFalse(StudentTransfer.objects.filter(target=lesson2, account=user1.profile).exists())

class AccountTest(TestCase):

    def setUp(self):
        self.account = mommy.make(Account, index_number="0001")
    
    def test_unicode(self):
        """ Requirement - __unicode__ method should include index number of object. """
        self.assertTrue(self.account.index_number in unicode(self.account))
        
    def test_get_plan(self):
        """ Assign account into group with one lesson and check get_plan content. """
        group = mommy.make(Group)
        lesson = mommy.make(Lesson)
        self.account.groups.add(group)
        lesson.group = group
        lesson.save()
        group.save()
        self.account.save()
        plan = self.account.get_plan()
        self.assertIn(lesson, Lesson.objects.all())
        self.assertIn(lesson, plan)
        
    def test_create_wrong_profile(self):
        """ Create profile with wrong index_number field. """
        try:
            new_account = mommy.make(Account, index_number = "abcdee1123")
            new_user = mommy.make(User)
        except ValidationError: # index number doesn't meet requirements
            return              # so it should throw ValidationError
        self.assertTrue(False)
    
    
    