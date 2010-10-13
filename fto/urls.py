from django.conf.urls.defaults import *

urlpatterns = patterns('fasterstronger.fto.views',
    # Example:
    (r'^(?P<username>[-_a-zA-Z ]+)/', 'plan'),
)
