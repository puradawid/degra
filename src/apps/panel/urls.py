from django.conf.urls import include, patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.PanelView.as_view(), name='panel'),
    url(r'^import_students/$', views.ImportStudentsView.as_view(), name='import_students'),
    url(r'^import_groups/$', views.ImportGroupsView.as_view(), name='import_groups'),
)