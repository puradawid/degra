#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models

## Represent single post (news from deanery) model
#
class Post(models.Model):
    title = models.CharField(max_length = 255, verbose_name = 'Tytuł')
    content = models.TextField(verbose_name = 'Treść')
    created = models.DateTimeField(auto_now_add=True, verbose_name = 'Utworzono')
    
    class Meta:
        app_label = "plan"
        verbose_name = 'Ogłoszenie'
        verbose_name_plural = 'Ogłoszenia'
    
    def __unicode__(self):
        return self.title
