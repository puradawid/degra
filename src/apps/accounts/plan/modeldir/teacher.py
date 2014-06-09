#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length = 35, verbose_name = 'Imię')
    surname = models.CharField(max_length = 35, verbose_name = 'Nazwisko')
    degree = models.CharField(max_length = 35, verbose_name = 'Stopień')
    email = models.CharField(max_length = 255, verbose_name = 'Email')
    
    class Meta:
        app_label = "plan"
        verbose_name = 'Nauczyciel'
        verbose_name_plural = 'Nauczyciele'
        
    def __unicode__(self):
        return self.degree + " " + self.name + " " + self.surname