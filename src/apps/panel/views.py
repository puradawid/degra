 #!/usr/bin/python
# -*- coding: utf-8 -*-

from django.views.generic import FormView
from django.contrib.auth.models import User
from apps.plan.models import Group, Post
from apps.accounts.models import Account
from apps.panel.forms import ImportCSVForm, NewsForm
from django.contrib import messages
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.core.urlresolvers import reverse
import csv
import os
from django.views.generic.base import TemplateView
import xml.etree.cElementTree as etree
import re
from django.core.exceptions import ValidationError
from apps.plan.modeldir.teacher import Teacher
from apps.plan.modeldir.course import Course
from apps.plan.modeldir.lesson import Lesson

class PanelView(TemplateView):
    template_name = 'panel/panel.html'

class ImportStudentsView(FormView):
    template_name = 'panel/import_students.html'
    form_class = ImportCSVForm
    success_url = '.'
    
    def form_valid(self, form):
        uploaded_file = form.cleaned_data['file']
        rows = list(csv.reader(uploaded_file))

        for row in rows:
            index_number = row[0]

            profile = Account.objects.get_or_create(index_number=index_number)[0]

            for group_name in row[1:]:    
                m = re.search('[a-zA-Z-]+(?!=\d)', group_name)
                if m:
                    group_prefix = m.group()
                else:
                    raise ValidationError('Not a valid group name!')

                group = Group.objects.get_or_create(name=group_name, semestr=1, field_of_study='INF', number=1)[0]
                
                # check if user is already in group
                if group in profile.groups.all():
                    continue

                profile.update_group(group, group_prefix)

        return super(ImportStudentsView, self).form_valid(form)

class ImportPlanView(TemplateView):
    template_name = 'panel/import_groups.html'
    
    def get_context_data(self, **kwargs):
        context = super(ImportPlanView, self).get_context_data(**kwargs)
        with open('plan.xml') as xmlfile:
            xmldata = xmlfile.read()
            count = import_groups_from_xml(xmldata)
            context['count'] = count
        return context

class AddNews(CreateView):
    template_name = 'panel/add_news.html'
    form_class = NewsForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(AddNews, self).get_context_data(**kwargs)
        context.update({
            # extra data goes here
            # 'key' : value
            'posts' : Post.objects.all().order_by('-created')
        })
        return context
    
class DeleteNews(DeleteView):
    model = Post
    template_name = 'panel/delete_news.html'
    
    def get_object(self, *args, **kwargs):
        obj = super(DeleteNews,self).get_object(*args,**kwargs)
        return obj
    
    def get_success_url(self):
        return reverse('add_news')
    
class EditNews(UpdateView):
    model = Post
    template_name = 'panel/edit_news.html'   
    form_class = NewsForm
    
    def get_object(self, *args, **kwargs):
        obj = super(EditNews, self).get_object(*args, **kwargs)
        return obj 
    
    def get_success_url(self):
        return reverse('add_news')

def import_groups_from_xml(xmldata):
    """
        Import groups from xmldata (file or webservice). Accepts string with xml data as parameter. Return number of imported groups.
        :param xmldata: string
        :returns count: int
    """
    count = 0
    xml_tree = etree.XML(xmldata)
    for lesson in xml_tree.iter('lesson'):
        course_name = lesson.find('name').text
        field = lesson.find('field').text
        semestr = int(lesson.find('semestr').text)
        start_hour = lesson.find('start_hour').text
        duration = lesson.find('duration').text
        day_of_week = lesson.find('day_of_week').text
        type = lesson.find('type').text
        group_name = lesson.find('group').text
        teacher_name = lesson.find('teacher').find('name').text
        teacher_surname = lesson.find('teacher').find('surname').text
        teacher_email = lesson.find('teacher').find('email').text
        
        teacher = Teacher.objects.get_or_create(name=teacher_name, surname=teacher_surname, email=teacher_email)[0]
        course = Course.objects.get_or_create(name=course_name)[0]
        group = Group.objects.get_or_create(name=group_name, field_of_study=field, semestr=semestr)[0]
        lesson = Lesson.objects.get_or_create(start_hour=start_hour, duration=duration, day_of_week=day_of_week, type=type, group=group, course=course, teacher=teacher)

        count += 1
        
    return count