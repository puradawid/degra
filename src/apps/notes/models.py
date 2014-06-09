from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from django.contrib.auth.models import User

## Serves as object filtering based on generic foreign key
class NoteMixin(object):

    ## @return user notes
    def for_user(self, user):
        return self.filter(author=user)

    ## @return notes related to generic foreign key object
    def for_object(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type=content_type, object_id=obj.id)

class PostQuerySet(QuerySet, NoteMixin):
    pass

## Overrides default Queryset class
class NoteManager(models.Manager, NoteMixin):
    def get_query_set(self):
        return PostQuerySet(self.model, using=self._db)

## Represent single note with generic foreign key so it isn't related to any model
class Note(models.Model):
    ## Creationg date stamp
    created = models.DateTimeField(auto_now_add=True)
    ## Note text content
    content = models.TextField(blank=True)
    ## Note author
    author = models.ForeignKey(User)
    
    ## Generic foreign key
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    ## Override default manager
    objects = NoteManager()

    def __unicode__(self):
        return self.content
