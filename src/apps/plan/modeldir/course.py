from django.db import models

class Course(models.Model):
    name = models.CharField(max_length = 100)
    
    class Meta:
        app_label = "plan"
    
    def __unicode__(self):
        return self.name