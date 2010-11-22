from django.conf.urls.defaults import *

urlpatterns = patterns('fasterstronger.fto.views',
    # Example:
    url(r'^(?P<username>[-_a-zA-Z ]+)/(?P<week>[\d+]+)/', 'plan', name='week_plan'),
    url(r'^(?P<username>[-_a-zA-Z ]+)/', 'plan', name='plan'),
)
