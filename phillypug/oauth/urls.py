from django.conf.urls import patterns, include, url
from oauth.views import OAuthLoginView, OAuthCallbackView

urlpatterns = patterns('',
    url(r'^login/$', OAuthLoginView.as_view(), name='login'),
    url(r'^callback/$', OAuthCallbackView.as_view(), name='callback'),
)
