from django.db import models

class Group(models.Model):
    FIELD_CHOICES = (
        ('INF', 'Informatyka'),
        ('MAT', 'Matematyka'),
    )
    field_of_study = models.CharField(max_length = 3, choices = FIELD_CHOICES, verbose_name = 'Kierunek')
    semestr = models.IntegerField(verbose_name = 'Semestr')
    name = models.CharField(max_length = 15, verbose_name = 'Nazwa')

    class Meta:
        app_label = "plan"
        unique_together = (('field_of_study', 'semestr', 'name'),)
        verbose_name = 'Grupa'
        verbose_name_plural = 'Grupy'

    def __unicode__(self):
        return "{0} - {1}{2}".format(self.name, self.field_of_study, self.semestr)

    def save(self, *args, **kwargs):
        # group name should be uppercase
        self.name = self.name.upper()
        super(Group, self).save(*args, **kwargs)