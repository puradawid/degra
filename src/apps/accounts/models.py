from django.db import models
from django.contrib.auth.models import User
from apps.plan.models import Group
from django.db.models.signals import post_save
import re

class Account(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    groups = models.ManyToManyField(Group)
    
    def __unicode__(self):
        return self.user.username
    
def create_account_for_new_user(sender, created, instance, **kwargs):
    if created:
        account = Account.objects.create(user=instance)
        
post_save.connect(create_account_for_new_user, User, dispatch_uid='create_account_for_new_user')

def get_index_number(self):
    m = re.search('(?!=[a-zA-Z])\d+$', self.username)
    if m:
        return m.group()
    return self.username

User.add_to_class("get_index_number", get_index_number)