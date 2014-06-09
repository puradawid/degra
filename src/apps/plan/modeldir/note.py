from django.db import models
from apps.plan.models import Lesson
from apps.accounts.models import Account

## Represent note created by student and assigned to specyfic lesson
#
class Note(models.Model):
    title = models.CharField(max_length = 255)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(Account)
    lesson = models.ForeignKey(Lesson)
    
    class Meta:
        app_label = "plan"
    
    def __unicode__(self):
        return self.title