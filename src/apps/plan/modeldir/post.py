from django.db import models
from group import Group

class Post(models.Model):
    title = models.CharField(max_length = 255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = "plan"
    
    def __unicode__(self):
        return self.title
