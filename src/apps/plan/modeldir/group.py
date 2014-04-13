from django.db import models

class Group(models.Model):
    TYPE_CHOICES = (
        ('PS', 'Pracownia specjalistyczna'),
        ('LAB', 'Laboratorium'),
        ('CW', 'Cwiczenia'),
        ('WYK', 'Wyklad'),
    )
    name = models.CharField(max_length = 4)
    type = models.CharField(max_length = 3, choices = TYPE_CHOICES)
    
    class Meta:
        app_label = "plan"
    
    def __unicode__(self):
        return self.name