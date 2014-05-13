from django.views.generic.list import ListView
from apps.plan.models import Lesson, Post
from apps.accounts.models import Account
from django.db.models import Q
from apps.plan.modeldir.note import Note

def get_groups_plan(field, semestr, groups, electives=None):
    """
        Returns plan for a selected groups
    """
    qgroups = Q()
    qelectives = Q()
    
    for value in groups:
        qgroups |= Q(group__name__iexact = value, group__field_of_study__iexact=field, group__semestr=semestr)

    if electives is not None:
        for value in electives:
            qelectives |= Q(group__name__iexact = value, group__semestr=0)

    return Lesson.objects.filter(qgroups | qelectives)

class PersonalizedPlanView(ListView):
    template_name = 'plan/plan.html'
    context_object_name = 'lesson_list'
    
    def complete_plan(self, plan):
        for lesson in plan:
            lesson.notes = Note.objects.filter(lesson=lesson, author=self.request.user.profile)
            print lesson.notes
        return plan
    
    def get_queryset(self):

        if 'index_number' in self.kwargs:
            profile = Account.objects.get(index_number=self.kwargs['index_number'])
        elif self.request.user.is_authenticated():
            profile = self.request.user.profile
        else:
            return get_groups_plan('INF', '1', ('cw1', 'ps1'))

        return self.complete_plan(profile.get_plan())

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
    
    def complete_plan(self, plan):
        for lesson in plan:
            lesson.notes = Note.objects.filter(lesson=lesson, author=self.request.user.profile)
        
        return plan
    
    def get_queryset(self):
        qgroups = Q()
        qelectives = Q()
        
        field = self.kwargs['field']
        semestr = self.kwargs['semestr']
        groups = self.kwargs['groups'].split('/')
        
        if "electives" in self.kwargs:
            electives = self.kwargs['electives'].split('/')
            return get_groups_plan(field, semestr, groups, electives)
        else:
            return get_groups_plan(field, semestr, groups)
        
        for value in groups:
            qgroups |= Q(group__name__iexact = value, group__field_of_study__iexact=field, group__semestr=semestr)

        if "electives" in self.kwargs:
            electives = self.kwargs['electives'].split('/')
            for value in electives:
                qelectives |= Q(group__name__iexact = value, group__semestr=0)

        return Lesson.objects.filter(qgroups | qelectives)

    def get_context_data(self, **kwargs):
        context = super(PlanView, self).get_context_data(**kwargs)
        context.update({
            # extra data goes here
            # 'key' : value
            'posts' : Post.objects.all().order_by('-created')
        })
        return context
    
    