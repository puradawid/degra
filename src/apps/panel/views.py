 #!/usr/bin/python
# -*- coding: utf-8 -*-

from django.views.generic import FormView
from django.contrib.auth.models import User
from apps.plan.models import Group
from apps.accounts.models import Account
from apps.panel.forms import ImportCSVForm
from django.contrib import messages
import csv
import os

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
        print result['errors']
        messages.error(self.request, ','.join(result['errors']), fail_silently=True)
        return super(ImportStudentsView, self).form_valid(form)

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