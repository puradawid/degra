from apps.plan.modeldir.group import Group
from apps.plan.modeldir.lesson import Lesson
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
import re

class Account(models.Model):
    index_number = models.CharField(primary_key=True, max_length=7)
    user = models.OneToOneField(User, blank=True, null=True, related_name='profile')
    groups = models.ManyToManyField(Group)
    
    def __unicode__(self):
        return self.index_number
    
    def update_group(self, group, group_prefix):
        # check if user is already in such type of group
        #try:
        self.groups.filter(name__regex='^%s' % group_prefix).delete()
        #except Group.DoesNotExist:
        #    pass

        self.groups.add(group)
        #self.groups.save()

    def get_plan(self):
        # get transfer list
        transfer_list = StudentTransfer.objects.filter(account=self)

        # include transferred lessons and exclude origin lessons
        lesson_list = Lesson.objects.filter(Q(group__in=self.groups.all()) | Q(id__in=transfer_list.values_list('target', flat=True)), ~Q(id__in=transfer_list.values_list('origin', flat=True)))
        
        return lesson_list
        
    def make_transfer(self, old_lesson, new_lesson):
        
        # check if transferred lessons are same
        if old_lesson == new_lesson:
            raise Exception('Transferred lessons are same!')

        # check if user attending to lesson that is going to transfer
        if old_lesson not in self.get_plan():
            raise Exception('User is not attending to the old lesson!')

        # check if user is not attending new lesson yet - shouldn't ever happen
        if new_lesson in self.get_plan():
            raise Exception('User is already attending to the new lessen')

        # check if transferred lessons have the same course
        if old_lesson.course != new_lesson.course:
            raise Exception('Lessons have different courses!')

        try:
            # check if lesson is already transfered
            transfer = StudentTransfer.objects.get(target=old_lesson, account=self)
            
            # if transfer exists origin is transfer origin, l1 -1> l2 -2> l3
            # that means after second transfer new transfer should point to origin lesson l1 -> l3 not l2 -> l3
            origin = transfer.origin
            # if new lesson is same as origin lesson remove transfer
            if new_lesson == origin:
                transfer.delete()
                return
            
        except StudentTransfer.DoesNotExist:
            origin = old_lesson
        
        StudentTransfer.objects.create(account=self, origin=origin, target=new_lesson)

def create_profile(sender, created, instance, **kwargs):
    if created:
        m = re.search('(?!=[a-zA-Z])\d+$', instance.username)
        if m:
            print m.group()
            account, acc_created = Account.objects.get_or_create(pk=m.group())
            account.user = instance
            account.save()
        else:
            raise ValidationError('Not a valid index number!')        

post_save.connect(create_profile, User, dispatch_uid='create_profile')

class StudentTransfer(models.Model):
    account = models.ForeignKey(Account)
    origin = models.ForeignKey(Lesson, related_name='origin')
    target = models.ForeignKey(Lesson, related_name='target')