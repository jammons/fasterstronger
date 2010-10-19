import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

from fasterstronger.fto.models import Plan
from fasterstronger.workouts.models import Lift, ActiveLift, LiftPR

def plan(request, username):
    ''' This method is the primary display method for showing user's 
    workout plans.
    '''
    template_vars = {}
    user = User.objects.get(username=username)

    # Calculate week
    today = datetime.date.today()
    plan = user.plan
    delta = datetime.date.today() - plan.cycle_start_date
    days = abs(delta.days)
    week = (days/7) + 1 #not zero indexed
    week_plan = plan.get_lifts(week)

    lifts = user.active_lifts.all()

    template_vars['user'] = user
    template_vars['week_plan'] = week_plan
    return render_to_response('fto/plan.html', locals())
