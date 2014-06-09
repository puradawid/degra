#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from course import Course
from teacher import Teacher
from group import Group

## Represent single lesson
#
# Every lesson is related to teacher, course and group.
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
    ## Start hour represent 'real' hour from 1 to 24
    start_hour = models.IntegerField(verbose_name = 'Godzina rozpoczęcia')
    duration = models.IntegerField(verbose_name = 'Czas trwania')
    day_of_week = models.IntegerField(choices = DAY_CHOICES, verbose_name = 'Dzień tygodnia')
    type = models.CharField(max_length = 3, choices = TYPE_CHOICES, verbose_name = 'Typ')
    course = models.ForeignKey(Course, verbose_name = 'Kurs')
    teacher = models.ForeignKey(Teacher, verbose_name = 'Nauczyciel')
    group = models.ForeignKey(Group, verbose_name = 'Grupa')
    
    class Meta:
        app_label = "plan"
        unique_together = (('type', 'course', 'group'),)
        verbose_name = 'Zajęcia'
        verbose_name_plural = 'Zajęcia'

    def __unicode__(self):
        return str(self.course) + " " + self.group.name
    
    ## Find avaible lesson transfers in same course scope. 
    # @return QuerySet with avaible lesson transfers
    def get_available_transfers(self):
        return Lesson.objects.filter(course=self.course, type=self.type).exclude(pk=self.pk)
