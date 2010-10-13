from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    (r'^[_-a-zA-Z]+/', include('fasterstronger.workouts.lift')),
)
