from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^password/', include('password_reset.urls')),
    url(r'^panel/', include('apps.panel.urls')),
    url(r'^', include('apps.plan.urls')),
)
