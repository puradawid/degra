from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    title = models.CharField(max_length = 255)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(User)
    
    class Meta:
        app_label = "plan"
    
    def __unicode__(self):
        return self.title
