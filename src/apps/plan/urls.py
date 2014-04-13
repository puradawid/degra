from django.conf.urls import include, patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.PlanView.as_view(), name='show_plan'),
)
