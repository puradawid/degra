from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from django.contrib.auth.models import User

class PostMixin(object):
    def for_user(self, user):
        return self.filter(author=user)

    def for_object(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type=content_type, object_id=obj.id)

class PostQuerySet(QuerySet, PostMixin):
    pass

class NoteManager(models.Manager, PostMixin):
    def get_query_set(self):
        return PostQuerySet(self.model, using=self._db)

class Note(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
    author = models.ForeignKey(User)
    
    # Generic foreign key
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    # Override default manager
    objects = NoteManager()

    def __unicode__(self):
        return self.content
