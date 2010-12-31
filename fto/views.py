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
    plan = user.plan

    week = request.GET.get('week', None)
    if week is None:
        # Calculate week
        today = datetime.date.today()
        delta = datetime.date.today() - plan.cycle_start_date
        days = delta.days
        week = days/7
        week = week + 1 #this isn't 0 indexed
    else:
        week = int(week)

    if week < 1:
        #TODO: add messaging to this
        return HttpResponse("No negative weeks")

    # Set template vars
    previous_week = week - 1
    next_week = week + 1

    #calculate week plan
    (week_plan, active_lifts) = plan.get_lifts(week)

    template_vars['user'] = user
    template_vars['week_plan'] = week_plan
    template_vars['active_lifts'] = active_lifts
    template_vars['week'] = week
    template_vars['next_week'] = '%s?week=%s' % (
        reverse('plan', args=[user]), next_week)
    if previous_week >= 1:
        template_vars['previous_week'] = '%s?week=%s' % (
            reverse('plan', args=[user]), previous_week)
    return render_to_response('fto/plan.html', template_vars)
