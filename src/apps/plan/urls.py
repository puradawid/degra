from django.conf.urls import patterns, url, include
from . import views

urlpatterns = patterns('',
    url(r'^i/(?P<index_number>\d+)/$', views.PersonalizedPlanView.as_view(), name='show_users_plan'),
    url(r'^(?P<field>[a-zA-Z]+)/(?P<semestr>\d+)/(?P<groups>[\w/-]+)/ob/(?P<electives>[\w/-]+)/$', views.PlanView.as_view(), name="show_group_plan_electives"),
    url(r'^(?P<field>[a-zA-Z]+)/(?P<semestr>\d+)/(?P<groups>[\w/-]+)/$', views.PlanView.as_view(), name="show_group_plan"),
    url(r'^transfer/(?P<pk>\d+)/', views.LessonPlan.as_view(), name='lesson_transfer'),
    url(r'^$', views.PersonalizedPlanView.as_view(), name='show_my_plan'),
)
