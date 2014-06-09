from apps.accounts.models import Account
from apps.panel.forms import ImportCSVForm, NewsForm
from apps.plan.modeldir.course import Course
from apps.plan.modeldir.lesson import Lesson
from apps.plan.models import Group, Post, Teacher
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import transaction
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
import csv
import re
import xml.etree.cElementTree as etree

## Render deanery panel main page
#
class PanelView(TemplateView):
    template_name = 'panel/panel.html'

## Responsible for handling importing students list from csv file
#
class ImportStudentsView(FormView):
    template_name = 'panel/import_students.html'
    form_class = ImportCSVForm
    success_url = '.'
    
    ## Process csv file
    def form_valid(self, form):
        rows = list(csv.reader(form.cleaned_data['file']))
        
        # file doesnt have errors... yet
        has_error = False
        
        # make transaction savepoint
        sid = transaction.savepoint()
        
        # iterate over all file rows
        for row in rows:
            index_number = row[0]
            
            # get or create account with current index number
            profile, created = Account.objects.get_or_create(pk=index_number)

            # iterate over all user groups from file
            # 1st cell is index number
            for group_name in row[1:]:
                
                # group name convention -> upper case
                group_name = group_name.upper()
                
                # check if group has proper name PrefixNumber, eg. PS1    
                if not re.match('^[a-zA-Z-]+\d+$', group_name):
                    # we have bad item over here
                    messages.error(self.request, "{0} posiada niepoprawna grupe {1}".format(index_number, group_name))
                    # mark file as broken
                    has_error = True
                    # but don't interrupt parsing
                    continue

                group, created = Group.objects.get_or_create(name=group_name, semestr=1, field_of_study='INF')

                # omit unchanged groups
                if group in profile.groups.all():
                    continue

                # if everything looks good update group
                profile.update_group(group)

        if has_error:
            # if form file has errors rollback transation
            transaction.savepoint_rollback(sid)
            messages.success(self.request, "Operacja przerwana!")
        else:
            # otherwise commit it
            transaction.savepoint_commit(sid)
            messages.success(self.request, "Zaimportowano!")

        return super(ImportStudentsView, self).form_valid(form)

## Responsible for handling importing lesson schedule from webservice
#
class ImportPlanView(TemplateView):
    template_name = 'panel/import_groups.html'
    
    def get_context_data(self, **kwargs):
        context = super(ImportPlanView, self).get_context_data(**kwargs)
        with open('src/plan.xml') as xmlfile:
            xmldata = xmlfile.read()
            count = import_groups_from_xml(xmldata)
            context['count'] = count
        return context

## Render and handle view for creating new post
#
class AddNews(CreateView):
    template_name = 'panel/add_news.html'
    form_class = NewsForm
    success_url = '.'
    
    ## Add list of created posts to current context
    #
    # @return contex with extra list of created posts
    def get_context_data(self, **kwargs):
        context = super(AddNews, self).get_context_data(**kwargs)
        context.update({
            # extra data goes here
            # 'key' : value
            'posts' : Post.objects.all().order_by('-created')
        })
        return context

## Render and handle view for deleting specified post
#
class DeleteNews(DeleteView):
    model = Post
    template_name = 'panel/delete_news.html'
    
    def get_object(self, *args, **kwargs):
        obj = super(DeleteNews,self).get_object(*args,**kwargs)
        return obj
       
    def get_success_url(self):
        return reverse('add_news')
    
## Render and handle view for update specified post
#    
class EditNews(UpdateView):
    model = Post
    template_name = 'panel/edit_news.html'   
    form_class = NewsForm
    
    def get_object(self, *args, **kwargs):
        obj = super(EditNews, self).get_object(*args, **kwargs)
        return obj 
    
    def get_success_url(self):
        return reverse('add_news')

## Handle xml data with informations about teachers, courses and groups.
#
# It's used to import schedule from external webservice
# 
# @param xmldata Data from file or external webservice
# @return Number of created objects 
# @todo Better way to process update
def import_groups_from_xml(xmldata):
    """
        Import groups from xmldata (file or webservice). Accepts string with xml data as parameter. Return number of imported groups.
        :param xmldata: string
        :returns count: int
    """

    count = 0
    xml_tree = etree.XML(xmldata)
    
    # setup transation in case of errors
    with transaction.atomic():
        for lesson in xml_tree.iter('lesson'):
            course_name = lesson.find('name').text
            field = lesson.find('field').text.upper()
            semestr = int(lesson.find('semestr').text)
            start_hour = lesson.find('start_hour').text
            duration = lesson.find('duration').text
            day_of_week = lesson.find('day_of_week').text
            type = lesson.find('type').text
            group_name = lesson.find('group').text.upper()
            teacher_name = lesson.find('teacher').find('name').text
            teacher_surname = lesson.find('teacher').find('surname').text
            teacher_email = lesson.find('teacher').find('email').text
    
            teacher = Teacher.objects.get_or_create(name=teacher_name, surname=teacher_surname, email=teacher_email)[0]
            course = Course.objects.get_or_create(name=course_name)[0]
            group = Group.objects.get_or_create(name=group_name, field_of_study=field, semestr=semestr)[0]
            
            # type, group and course determine certain lesson
            lesson, created = Lesson.objects.get_or_create(type=type, group=group, course=course, defaults={'start_hour':start_hour, 'duration':duration, 'day_of_week':day_of_week, 'type':type, 'teacher':teacher})
    
            if created:
                count += 1
            else:
                # TODO:
                #    - changed flag
                #    - better way to process update
                
                # if lesson is not created it needs to be updated 
                lesson.start_hour = start_hour
                lesson.duration = duration
                lesson.day_of_week = day_of_week
                lesson.type = type
                lesson.teacher = teacher
                lesson.save()
        
    return count