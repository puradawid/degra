from django.db import models

class Group(models.Model):
    TYPE_CHOICES = (
        ('PS', 'Pracownia specjalistyczna'),
        ('LAB', 'Laboratorium'),
        ('CW', 'Cwiczenia'),
        ('WYK', 'Wyklad'),
    )
    FIELD_CHOICES = (
        ('INF', 'Informatyka'),
        ('MAT', 'Matematyka'),
    )
    field_of_study = models.CharField(max_length = 3, choices = FIELD_CHOICES)
    semestr = models.IntegerField()
    name = models.CharField(max_length = 15)
    
    number = models.IntegerField()
    type = models.CharField(max_length = 3, choices = TYPE_CHOICES)

    class Meta:
        app_label = "plan"

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = "{0}{1}".format(self.number, self.type)
            print self.name
        
        super(Group, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return "{0} - {1}{2}".format(self.name, self.field_of_study, self.semestr)
