from django.conf.urls import include, patterns, url
from . import views

urlpatterns = patterns('', 
    url(r'^import_students/$', views.ImportStudentsView.as_view(), name='import_students'),
)