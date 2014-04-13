from django.db import models
from django.contrib.auth.models import User
from apps.plan.models import Group

class Account(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    groups = models.ManyToManyField(Group)
    
    def __unicode__(self):
        return self.user.username