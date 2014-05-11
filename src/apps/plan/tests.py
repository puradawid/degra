from django.test import TestCase
from django.core.management import call_command
from apps.accounts.models import UserToLesson
from apps.plan.modeldir.lesson import Lesson
from django.contrib.auth.models import User

class PlanTestCase(TestCase):
    
    def setUp(self):
        # Load fixtures
        call_command('loaddata', 'account', verbosity=0)
        call_command('loaddata', 'plan', verbosity=0)
        call_command('loaddata', 'usertolesson', verbosity=0)
        
        UserToLesson.objects.create(user=User.objects.get(pk=2), lesson=Lesson.objects.get(pk=2))

    def test_notes_relations(self):
        user2_notes = UserToLesson.objects.get(lesson__pk=2, user__pk=2).notes
        self.assertEqual(user2_notes.count(), 0)
        user1_notes = UserToLesson.objects.get(lesson__pk=2, user__pk=1).notes
        self.assertEqual(user1_notes.count(), 1)

    def test_lesson_relations(self):
        user2_lesson = UserToLesson.objects.filter(user__pk=2)
        self.assertEqual(user2_lesson.count(), 1)
        user1_lesson = UserToLesson.objects.filter(user__pk=1)
        self.assertEqual(user1_lesson.count(), 3)