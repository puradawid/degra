#!/usr/bin/python
# -*- coding: utf-8 -*-

from apps.plan.modeldir.group import Group
from apps.plan.modeldir.lesson import Lesson
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
import re

class Account(models.Model):
    index_number = models.CharField(primary_key=True, max_length=7, verbose_name = 'Numer indeksu')
    user = models.OneToOneField(User, blank=True, null=True, related_name='profile', verbose_name = 'Użytkownik')
    groups = models.ManyToManyField(Group, verbose_name = 'Grupy')
    
    def __unicode__(self):
        return self.index_number
    
    def update_group(self, group):
        # verify group name
        m = re.search('^[a-zA-Z-]+(?=\d+$)', group.name)
        if m:
            group_prefix = m.group()
        else:
            raise Exception('Not a valid group')
        
        try:
            # fix transfers
            
            # find old group
            old_group = self.groups.get(name__regex='^%s' % group_prefix)
            # find transfers from old group
            transfers = StudentTransfer.objects.filter(origin__group=old_group)

            for transfer in transfers:
                # if transferred lesson is in new group remove transfer
                if transfer.target.group == group:
                    transfer.delete()
                else:
                    # attach origin to lesson from new group
                    transfer.origin = Lesson.objects.get(course=transfer.origin.course, type=transfer.origin.type, group=group)
                    
        except Group.DoesNotExist:
            pass
        
        # check if user is already in such type of group
        if self.groups.filter(name__regex='^%s' % group_prefix).exists():
            self.groups.remove(self.groups.get(name__regex='^%s' % group_prefix))
        
        # finally add new group
        self.groups.add(group)

    def get_plan(self):
        # get transfer list
        transfer_list = StudentTransfer.objects.filter(account=self)

        # include transferred lessons and exclude origin lessons
        lesson_list = Lesson.objects.filter(Q(group__in=self.groups.all()) | Q(pk__in=transfer_list.values_list('target', flat=True)), ~Q(id__in=transfer_list.values_list('origin', flat=True)))

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
            raise Exception('User is already attending to the new lesson!')

        # check if transfer is within same course, RW->RW
        if old_lesson.course != new_lesson.course:
            raise Exception('Lessons have different courses!')
        
        # check if transfer is within same type, eg PS->PS
        if old_lesson.type != new_lesson.type:
            raise Exception('Lessons have different types!')

        try:
            # check if lesson is already transferred
            transfer = StudentTransfer.objects.get(target=old_lesson, account=self)
            # if new lesson is same as origin lesson remove transfer
            if new_lesson == transfer.origin:
                transfer.delete()
                return
            else:
                # if transfer exists origin is transfer origin, l1 -1> l2 -2> l3
                # that means after second transfer new transfer should point to origin lesson l1 -> l3 not l2 -> l3
                transfer.target = new_lesson
                transfer.save()
                return
            
        except StudentTransfer.DoesNotExist:
            origin = old_lesson
        
        StudentTransfer.objects.create(account=self, origin=origin, target=new_lesson)
        
    class Meta:
        verbose_name = 'Konto'
        verbose_name_plural = 'Konta'

def create_profile(sender, created, instance, **kwargs):
    if created:
        
        # TODO:
        #     - staff accounts
        
        m = re.search('(?!=[a-zA-Z])\d+$', instance.username)
        if m:
            # attach account to created user
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
