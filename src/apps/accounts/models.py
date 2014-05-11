from django.db import models
from django.contrib.auth.models import User
from apps.plan.models import Group
from django.db.models.signals import post_save
from apps.plan.models import Lesson, Note
import re
from django.core.exceptions import ValidationError

class Account(models.Model):
    index_number = models.CharField(primary_key=True, max_length=7)
    user = models.OneToOneField(User, blank=True, null=True, related_name='profile')
    groups = models.ManyToManyField(Group)
    
    def __unicode__(self):
        return self.index_number

def create_profile(sender, created, instance, **kwargs):
    if created:
        m = re.search('(?!=[a-zA-Z])\d+$', instance.username)
        if m:
            print m.group()
            account = Account.objects.get_or_create(index_number=m.group())
            account[0].user = instance
            account[0].save()
        else:
            raise ValidationError('Not a valid index number!')        
        
post_save.connect(create_profile, User, dispatch_uid='create_profile')

class UserToLesson(models.Model):
    account = models.ForeignKey(Account, blank=True, null=True)
    lesson = models.ForeignKey(Lesson)
    notes = models.ManyToManyField(Note)