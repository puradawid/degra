from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length = 35)
    surname = models.CharField(max_length = 35)
    degree = models.CharField(max_length = 35)
    email = models.CharField(max_length = 255)
    
    class Meta:
        app_label = "plan"
    
    def __unicode__(self):
        return self.name + self.surname