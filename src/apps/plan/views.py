from apps.accounts.models import Account
from apps.plan.models import Lesson, Post, Note, Group
from django.db.models import Q
from django.views.generic.list import ListView

def nameiexact(name_list):
    q_list = map(lambda n: Q(name__iexact=n), name_list)
    q_list = reduce(lambda a, b: a | b, q_list)

    return q_list

def add_notes(profile, plan):
    for lesson in plan:
        lesson.notes = Note.objects.filter(lesson=lesson, author=profile)        
    return plan

class PersonalizedPlanView(ListView):
    template_name = 'plan/plan.html'
    context_object_name = 'lesson_list'
    
    def get_queryset(self):

        if 'index_number' in self.kwargs:
            profile = Account.objects.get(index_number=self.kwargs['index_number'])
        elif self.request.user.is_authenticated():
            profile = self.request.user.profile
        else:
            groups = Group.objects.filter(Q(field_of_study='INF', semestr=1), nameiexact(['cw1', 'ps1']))
            return Lesson.objects.filter(group__in=groups)
        
        lesson_list = profile.get_plan()
        
        if self.request.user.is_authenticated():
            # add notes for logged user
            lesson_list = add_notes(self.request.user.profile, lesson_list)

        return lesson_list

    def get_context_data(self, **kwargs):
        context = super(PersonalizedPlanView, self).get_context_data(**kwargs)
        context.update({
            # extra data goes here
            # 'key' : value
            'posts' : Post.objects.all().order_by('-created')
        })
        return context

class PlanView(ListView):
    template_name = 'plan/plan.html'
    context_object_name = 'lesson_list'
    
    def get_queryset(self):
        
        field = self.kwargs['field']
        semestr = self.kwargs['semestr']
        groups = self.kwargs['groups'].split('/')
        
        qgroups = Q(Q(field_of_study__iexact=field, semestr=semestr), nameiexact(groups))
        
        if "electives" in self.kwargs:
            electives = self.kwargs['electives'].split('/')
            qgroups |= Q(Q(semestr=0), nameiexact(electives))
        
        lesson_list = Lesson.objects.filter(group__in=Group.objects.filter(qgroups))
        
        if self.request.user.is_authenticated():
            # add notes for logged user
            lesson_list = add_notes(self.request.user.profile, lesson_list)

        return lesson_list
    
    def get_context_data(self, **kwargs):
        context = super(PlanView, self).get_context_data(**kwargs)
        context.update({
            # extra data goes here
            # 'key' : value
            'posts' : Post.objects.all().order_by('-created')
        })
        return context
    
    