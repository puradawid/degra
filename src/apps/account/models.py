from django.db import models
from django.contrib.auth.models import User
from apps.group.models import Group

class Account(models.Model):
    user = models.OneToOneField('auth.User', related_name='profile')
    groups = models.ManyToManyField(Group)
    
    def __unicode__(self):
        return self.user.username