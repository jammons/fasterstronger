from django.db import models
from django.contrib.auth.models import User

from fasterstronger.utils import round_to_plate_size

DEFAULT_PLATE_SIZE = 2.5

WEEK_SCHEME = {
    1 : [(5,.65), (5,.75), ('amrap',.85)],
    2 : [(3,.70), (3,.80), ('amrap',.90)],
    3 : [(5,.75), (3,.85), ('amrap',.95)],
    4 : [(5,.40), (5,.50), (5,.60)]
}

class Plan(models.Model):
    user = models.OneToOneField(User, related_name='plan')
    weekly_workouts = models.IntegerField() #number of times in the gym in a week
    cycle_start_date = models.DateField()

    def get_lifts(self, week):
        #return the active lifts for this user
        lifts = self.user.active_lifts.all()

        scheme = WEEK_SCHEME[week]
        days = []
        for lift in lifts:
            reduced_max = .9 * float(lift.get_onerm().weight)
            days.append({
                'name': lift.lift.name,
                'scheme': 
                [(scheme[0][0], round_to_plate_size(scheme[0][1]*float(reduced_max), 2.5)),
                (scheme[1][0], round_to_plate_size(scheme[1][1]*float(reduced_max), 2.5)),
                (scheme[2][0], round_to_plate_size(scheme[2][1]*float(reduced_max), 2.5))]
            })
        return days
