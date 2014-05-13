from django.db import models

class Group(models.Model):
    FIELD_CHOICES = (
        ('INF', 'Informatyka'),
        ('MAT', 'Matematyka'),
    )
    field_of_study = models.CharField(max_length = 3, choices = FIELD_CHOICES)
    semestr = models.IntegerField()
    name = models.CharField(max_length = 15)

    class Meta:
        app_label = "plan"
        unique_together = (('field_of_study', 'semestr', 'name'),)

    def __unicode__(self):
        return "{0} - {1}{2}".format(self.name, self.field_of_study, self.semestr)
