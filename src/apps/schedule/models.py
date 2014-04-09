from django.db import models
from apps.group.models import Group

class Course(models.Model):
    name = models.CharField(max_length = 100)
    
    def __unicode__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length = 35)
    surname = models.CharField(max_length = 35)
    degree = models.CharField(max_length = 35)
    email = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return self.name + self.surname
    
class Lesson(models.Model):
    TYPE_CHOICES = (
        ('PS', 'Pracownia specjalistyczna'),
        ('LAB', 'Laboratorium'),
        ('CW', 'Cwiczenia'),
        ('WYK', 'Wyklad'),
    )
    DAY_CHOICES = (
        (1, 'Poniedzialek'),
        (2, 'Wtorek'),
        (3, 'Sroda'),
        (4, 'Czwartek'),
        (5, 'Piatek'),
        (6, 'Sobota'),
        (7, 'Niedziela'),
    )
    start_hour = models.IntegerField()
    end_hour = models.IntegerField()
    day_of_week = models.IntegerField(choices = DAY_CHOICES)
    type = models.CharField(max_length = 3, choices = TYPE_CHOICES)
    course = models.ForeignKey(Course)
    teacher = models.ForeignKey(Teacher)
    group = models.ForeignKey(Group)
    
    def __unicode__(self):
        return self.course + " " + self.group.name
