from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'home.views.index', name='index'),
    url(r'^oauth/', include('oauth.urls', namespace='oauth')),
    url(r'^admin/', include(admin.site.urls)),
)
