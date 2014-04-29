from django.views.generic.list import ListView
from apps.plan.models import Lesson
from apps.accounts.models import UserToLesson
from django.db.models import Q

class PersonalizedPlanView(ListView):
    template_name = 'plan/plan.html'
    context_object_name = 'lesson_list'
    
    def get_queryset(self):
        lesson_list = list()

        if 'index_number' in self.kwargs:
            utllist = UserToLesson.objects.filter(user__profile__index_number=self.kwargs['index_number'])
        elif self.request.user.is_authenticated():
            utllist = UserToLesson.objects.filter(user=self.request.user)
        else: # tymczasowe rozwiazanie
            pview = PlanView()
            pview.kwargs={'field': 'inf', 'semestr': '1', 'groups': 'cw1'}
            return pview.get_queryset()

        for obj in utllist:
            lesson = obj.lesson
            if self.request.user.is_authenticated() and obj.user == self.request.user:
                lesson.notes = obj.notes
            lesson_list.append(lesson)

        return lesson_list

    def get_context_data(self, **kwargs):
        context = super(PersonalizedPlanView, self).get_context_data(**kwargs)
        context.update({
            # extra data goes here
            # 'key' : value
        })
        return context

class PlanView(ListView):
    template_name = 'plan/plan.html'
    context_object_name = 'lesson_list'
    
    def get_queryset(self):
        qgroups = Q()
        qelectives = Q()
        
        field = self.kwargs['field']
        semestr = self.kwargs['semestr']
        groups = self.kwargs['groups'].split('/')
        
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
        })
        return context
    