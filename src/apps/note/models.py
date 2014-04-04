from django.db import models
from apps.account.models import Student

class Note(models.Model):
    title = models.CharField(max_length = 255)
    created = models.DateTimeField(auto_now=True)
    content = models.TextField()
    student = models.ForeignKey(Student)
    
    def __unicode__(self):
        return self.title
