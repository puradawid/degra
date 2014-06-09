from django.contrib import messages, auth
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.list import ListView

from apps.accounts.models import Account
from apps.plan.models import Lesson, Post
from apps.notes.models import Note
from apps.notes.forms import NoteForm
from django.contrib.contenttypes.models import ContentType

def add_notes(user, plan):
    all_notes = Note.objects.for_user(user)
    
    for lesson in plan:
        lesson.note = all_notes.for_object(lesson).first()

    return plan

class PersonalizedPlanView(ListView):
    template_name = 'plan/plan.html'
    context_object_name = 'lesson_list'
    
    def get_queryset(self):

        if 'index_number' in self.kwargs:
            # if user provide index number then select profile with that index number
            profile = Account.objects.get(index_number=self.kwargs['index_number'])
        elif self.request.user.is_authenticated():
            # if user is logged in take his profile
            profile = self.request.user.profile
        else:
            # otherwise show default plan
            return Lesson.objects.filter(group__name__in=["CW1", "PS1"], group__field_of_study='INF', group__semestr=1)

        # get plan for given profile
        lesson_list = profile.get_plan()

        if self.request.user.is_authenticated():
            # add notes for logged user
            lesson_list = add_notes(self.request.user, lesson_list)
            
        return lesson_list

    def get_context_data(self, **kwargs):
        context = super(PersonalizedPlanView, self).get_context_data(**kwargs)
        context.update({
            # extra data goes here
            # 'key' : value
            'noteform' : NoteForm(),
            'posts' : Post.objects.all().order_by('-created')
        })
        return context
    
    def post(self, request, *args, **kwargs):
        
        form = NoteForm(request.POST)
        
        if form.is_valid():
            lesson = Lesson.objects.get(pk=form.cleaned_data['lesson'])
            type = ContentType.objects.get_for_model(lesson)
            (note, created) = Note.objects.get_or_create(author=auth.get_user(request), content_type=type, object_id=lesson.id, defaults={'content': form.cleaned_data['content']})
            if not created:
                note.content = form.cleaned_data['content']
                note.save()
            print note
        
        return redirect('.')  

class PlanView(ListView):
    template_name = 'plan/plan.html'
    context_object_name = 'lesson_list'
    
    def get_queryset(self):
        
        field = self.kwargs['field'].upper()
        semestr = self.kwargs['semestr']
        
        # convert group name to uppercase
        groups = [x.upper() for x in self.kwargs['groups'].split('/')]
        
        # find all lessons from given groups
        q = Q(group__name__in=groups, group__semestr=semestr, group__field_of_study=field)
        

        if "electives" in self.kwargs:
            # include elective lessons
            electives = [x.upper() for x in self.kwargs['electives'].split('/')]
            q |= Q(group__name__in=electives, group__semestr=0)

        lesson_list = Lesson.objects.filter(q)
        
        if self.request.user.is_authenticated():
            # add notes for logged user
            lesson_list = add_notes(self.request.user, lesson_list)
        
        return lesson_list

    def get_context_data(self, **kwargs):
        context = super(PlanView, self).get_context_data(**kwargs)
        context.update({
            # extra data goes here
            # 'key' : value
            'posts' : Post.objects.all().order_by('-created')
        })
        return context

class LessonPlan(ListView):
    template_name = 'plan/lesson_plan.html'
    context_object_name = 'lesson_list'

    def get_queryset(self):
        try:
            return self.request.user.profile.get_plan().get(pk = self.kwargs['pk']).get_available_transfers()
        except Lesson.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        
        try:
            old_lesson = Lesson.objects.get(pk=kwargs['pk'])
            new_lesson = Lesson.objects.get(pk=request.POST['new_lesson'])
    
            self.request.user.profile.make_transfer(old_lesson, new_lesson)
            
            return HttpResponseRedirect(reverse('show_my_plan'))
        except Exception as e:
            messages.error(request, e)
        
        return self.get(request, *args, **kwargs)  