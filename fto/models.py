from django.db import models
from django.contrib.auth.models import User

from fasterstronger.workouts.models import Lift

WEEK_SCHEME = {
    1 : [(5,.65), (5,.75), ('amrap',.85)],
    2 : [(3,.70), (3,.80), ('amrap',.90)],
    3 : [(5,.75), (5,.85), ('amrap',.95)],
    4 : [(5,.40), (5,.50), (5*.60)]
}



class Plan(models.Model):
    user = models.OneToOneField(User, related_name='plan')
    weekly_workouts = models.IntegerField() #number of times in the gym in a week
    active_lifts = models.ManyToManyField(Lift)
    cycle_start_date = models.DateField()

    def get_lifts(self, week):
        #return the lifts for the given week of the cycle
        lifts = self.active_lifts
        lift_prs = [lift.current_pr() for lift in lifts]
        scheme = WEEK_SCHEME[week]
        days = []
        for lift_pr in lift_prs:
            reduced_max = .9 * lift_pr
            days += [
                (scheme[0][0], scheme[0][1]*reduced_max),
                (scheme[1][0], scheme[1][1]*reduced_max),
                (scheme[2][0], scheme[2][1]*reduced_max)
            ]
        return days

