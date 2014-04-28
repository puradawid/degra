from django.views.generic.list import ListView
from apps.plan.models import Lesson
from apps.accounts.models import UserToLesson

class PlanView(ListView):
    template_name = 'plan/plan.html'
    context_object_name = 'lesson_list'
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            lessonlist = list()
            utllist = UserToLesson.objects.filter(user=self.request.user)
            for obj in utllist:
                lesson = obj.lesson
                lesson.notes = obj.notes
                lessonlist.append(lesson)
            
            return lessonlist

    def get_context_data(self, **kwargs):
        context = super(PlanView, self).get_context_data(**kwargs)
        context.update({
            # extra data goes here
            # 'key' : value
        })
        return context
    
    