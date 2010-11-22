import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from fasterstronger.fto.models import Plan, Lift, ActiveLift, LiftPR

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

    if week < 1:
        #TODO: add messaging to this
        return HttpResponse("No negative weeks")
    week = int(week)
    previous_week = week - 1
    next_week = week + 1
    week_plan = plan.get_lifts(week)

    lifts = user.active_lifts.all()

    template_vars['user'] = user
    template_vars['week_plan'] = week_plan
    template_vars['week'] = week
    template_vars['next_week'] = reverse('week_plan', args=[user, week])
        
    template_vars['previous_week'] = previous_week
    return render_to_response('fto/plan.html', template_vars)
