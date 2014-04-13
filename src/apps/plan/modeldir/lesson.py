from django.db import models
from course import Course
from teacher import Teacher
from group import Group

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
    
    class Meta:
        app_label = "plan"

    def __unicode__(self):
        return self.course + " " + self.group.name