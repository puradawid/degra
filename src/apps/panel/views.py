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
from braces.views._access import LoginRequiredMixin

class PanelView(TemplateView):
    template_name = 'panel/panel.html'

class ImportStudentsView(FormView):
    template_name = 'panel/import_students.html'
    form_class = ImportCSVForm
    success_url = '.'
    
    def form_valid(self, form):
        uploaded_file = form.cleaned_data['file']
        handle_uploaded_file(uploaded_file)
        with open('uploads/' + uploaded_file.name) as csvfile:
            result = import_students_from_csv(csvfile)
        remove_uploaded_file(uploaded_file)
        messages.success(self.request, 'Zaimportowano ' + str(result['count']) + ' studentów', fail_silently=True)
        # print result['errors'] TODO: Log errors or sth
        # messages.error(self.request, ','.join(result['errors']), fail_silently=True)
        return super(ImportStudentsView, self).form_valid(form)

class ImportGroupsView(TemplateView):
    template_name = 'panel/import_groups.html'
    
    def get_context_data(self, **kwargs):
        context = super(ImportGroupsView, self).get_context_data(**kwargs)
        with open('grupy.xml') as xmlfile:
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
    
def handle_uploaded_file(uploaded_file):
    """
        Save uploaded file
    """
    filename = uploaded_file.name
    with open('uploads/' + filename, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
            
def remove_uploaded_file(uploaded_file):
    """
        Remove uploaded file from server
    """
    filename = uploaded_file.name
    os.remove('uploads/' + filename)

def import_students_from_csv(csvfile):
    """
        Import students objects from csvfile. Accepts file object as parameter (open file). Return dictionary with 'count' and 'errors' keys
        :param csvfile: file
        :returns count: dictionary - key 'count': int, key 'messages': list of strings
    """
    students_reader = csv.DictReader(csvfile)
    result = {'count': 0, 'errors': []}
    for row in students_reader:
        if User.objects.filter(username=row['Indeks']).exists() == False:
            user = User.objects.create(username=row['Indeks'])
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            account = Account.objects.create(user=user)
            try:
                group = Group.objects.get(name=row['Grupa'])
                account.groups.add(group)
            except Exception:
                result['errors'].append('Grupa ' + row['Grupa'] + ' nie istnieje w bazie')
                
            account.save()
            result['count'] += 1
    return result

def import_groups_from_xml(xmldata):
    """
        Import groups from xmldata (file or webservice). Accepts string with xml data as parameter. Return number of imported groups.
        :param xmldata: string
        :returns count: int
    """
    count = 0
    xml_tree = etree.XML(xmldata)
    for group in xml_tree.iter('grupa'):
        name = group.find('nazwa').text
        type = group.find('typ').text
        g = Group.objects.create(name=name, type=type)
        g.save()
        count += 1
        
    return count