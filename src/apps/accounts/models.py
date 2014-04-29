from django.db import models
from django.contrib.auth.models import User
from apps.plan.models import Group
from django.db.models.signals import post_save
from apps.plan.models import Lesson, Note
import re
from django.core.exceptions import ValidationError

class UserToLesson(models.Model):
    user = models.ForeignKey(User)
    lesson = models.ForeignKey(Lesson)
    notes = models.ManyToManyField(Note)

class Account(models.Model):
    index_number = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, related_name='profile')
    groups = models.ManyToManyField(Group)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            m = re.search('(?!=[a-zA-Z])\d+$', self.user.username)
            if m:
                self.index_number = m.group()
            else:
                raise ValidationError('Not a valid index number!')
        
        super(Account, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username

def create_profile(sender, created, instance, **kwargs):
    if created:
        Account.objects.get_or_create(user=instance)
        
post_save.connect(create_profile, User, dispatch_uid='create_profile')