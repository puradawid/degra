from apps.accounts.models import Account
from apps.plan.models import Lesson, Post, Note
from django.db.models import Q
from django.views.generic.list import ListView

def add_notes(profile, plan):
    # TODO:
    #    - find better way to handle notes
    for lesson in plan:
        lesson.notes = Note.objects.filter(lesson=lesson, author=profile)
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
    
    