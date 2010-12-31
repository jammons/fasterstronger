from django.conf.urls.defaults import *

urlpatterns = patterns('fasterstronger.fto.views',
    url(r'^(?P<username>[-_a-zA-Z ]+)/$', 'plan', name='plan'),
)
