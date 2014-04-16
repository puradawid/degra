from django.views.generic import FormView
from django.contrib.auth.models import User
from apps.plan.models import Group
from apps.panel.forms import ImportCSVForm

class ImportStudentsView(FormView):
    template_name = 'panel/import_students.html'
    form_class = ImportCSVForm
    success_url = '/'
    
    def form_valid(self, form):
        # Handle import students
        return super(ImportStudentsView, self).form_valid(form)