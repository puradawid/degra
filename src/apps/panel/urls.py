from django.conf.urls import include, patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.PanelView.as_view(), name='panel'),
    url(r'^import_students/$', views.ImportStudentsView.as_view(), name='import_students'),
    url(r'^import_groups/$', views.ImportGroupsView.as_view(), name='import_groups'),
    url(r'^news/', include([
        url(r'^$', views.AddNews.as_view(), name='add_news'),
        url(r'^(?P<pk>\d+)/delete$', views.DeleteNews.as_view(), name='delete_news'),
        url(r'^(?P<pk>\d+)/edit$', views.EditNews.as_view(), name='edit_news'),
    ]))
)