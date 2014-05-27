from django.test import TestCase

from model_mommy import mommy

from apps.plan.models import Course, Group, Note, Lesson, Post, Teacher
from apps.accounts.models import Account

class TestNoteModel(TestCase):
    
    def setUp(self):
        self.author = mommy.make(Account, index_number="0001")
        self.lesson = mommy.make(Lesson)
        self.note = mommy.make(Note)
        
        self.note.author = self.author
        self.note.lesson = self.lesson
        
    def test_save_note(self):
        self.note.save()
        self.assertIn(self.note, Note.objects.all())

    def test_take_author(self):
        self.assertEquals(self.note.author, self.author)
        
    def test_take_lesson(self):
        self.assertEquals(self.note.lesson, self.lesson)
        
    def test_unicode(self):
        self.assertIn(self.note.title, unicode(self.note))
        
class CourseTest(TestCase):
    
    def setUp(self):
        self.course = mommy.make(Course)
    
    def test_unicode(self):
        self.assertIn(self.course.name, unicode(self.course))
        
class GroupTest(TestCase):
    
    def setUp(self):
        self.group = mommy.make(Group, name="kdjasklfdsklfhdsjkhf")
        self.group.save()
    
    def test_name(self):
        self.assertEqual(self.group.name, self.group.name.upper())
        
    def test_unicode(self):
        unicode_group = unicode(self.group)
        self.assertIn(self.group.name, unicode_group)
        self.assertIn(self.group.field_of_study, unicode_group)
        self.assertIn(str(self.group.semestr), unicode_group)

class PostTest(TestCase):
    
    def setUp(self):
        self.post = mommy.make(Post)
    
    def test_unicode(self):
        self.assertIn(self.post.title, unicode(self.post))

class TeacherTest(TestCase):
    
    def setUp(self):
        self.teacher = mommy.make(Teacher)
    
    def test_unicode(self):
        self.assertIn(self.teacher.name, unicode(self.teacher))
        self.assertIn(self.teacher.surname, unicode(self.teacher))
        
class LessonTest(TestCase):
    
    def setUp(self):
        self.group = mommy.make(Group)
        self.lesson = mommy.make(Lesson)
        self.lesson.group = self.group
    
    def test_unicode(self):
        self.assertIn(str(self.lesson.course), unicode(self.lesson))
        self.assertIn(self.group.name, unicode(self.lesson))
        
    def test_get_available_transfers(self):
        similiar_lesson = mommy.make(Lesson, course=self.lesson.course, type=self.lesson.type)
        self.assertIn(similiar_lesson, self.lesson.get_available_transfers())