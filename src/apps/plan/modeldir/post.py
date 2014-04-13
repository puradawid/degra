from django.db import models

class Post(models.Model):
    title = models.CharField(max_length = 255)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    
    class Meta:
        app_label = "plan"
    
    def __unicode__(self):
        return self.name