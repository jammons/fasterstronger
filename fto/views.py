from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

from fasterstronger.fto.models import Plan
from fasterstronger.workouts.models import Lift, ActiveLift, LiftPR

def plan(request, username):
    ''' This method is the primary display method for showing user's 
    workout plans.
    '''
    user = User.objects.get(username=username)

    render_to_response('plan.html', user)
