from django.db import models
from django.contrib.auth.models import User
from apps.plan.models import Group
from django.db.models.signals import post_save
from apps.plan.models import Lesson, Note
import re

class UserToLesson(models.Model):
    user = models.OneToOneField(User)
    lesson = models.OneToOneField(Lesson)
    notes = models.ManyToManyField(Note)

class Account(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    groups = models.ManyToManyField(Group)
    
    def __unicode__(self):
        return self.user.username
    
def create_profile(sender, created, instance, **kwargs):
    if created:
        Account.objects.create(user=instance)
        
post_save.connect(create_profile, User, dispatch_uid='create_profile')

def get_index_number(self):
    m = re.search('(?!=[a-zA-Z])\d+$', self.username)
    if m:
        return m.group()
    return "0"

User.add_to_class("get_index_number", get_index_number)