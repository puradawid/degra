from django.db import models

class Course(models.Model):
    name = models.CharField(max_length = 100, verbose_name = 'Nazwa')
    
    class Meta:
        app_label = "plan"
        verbose_name = 'Kurs'
        verbose_name_plural = 'Kursy'
    
    def __unicode__(self):
        return self.name