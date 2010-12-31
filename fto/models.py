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

    def get_working_weight(self, active_lift, cycle):
        ''' Returns the working weight calculated by lift and cycle. '''
        weight = float(active_lift.get_onerm().weight) * .9
        # Need to add extra weight past first cycle
        weight = weight + (float(active_lift.increment) * cycle)
        return weight

    def get_lifts(self, week):
        #return the active lifts for this user
        lifts = self.user.active_lifts.all()
        cycle = (week-1)/4 #calculate cycles
        week = week % 4
        if week == 0: week = 4 #is there a better way to do this

        scheme = WEEK_SCHEME[week]
        days = []
        for lift in lifts:
            working_weight = self.get_working_weight(lift, cycle)
            lift.working_weight = working_weight
            days.append({
                'name': lift.lift.name,
                'scheme': 
                [(scheme[0][0], round_to_plate_size(scheme[0][1]*float(working_weight), 2.5)),
                (scheme[1][0], round_to_plate_size(scheme[1][1]*float(working_weight), 2.5)),
                (scheme[2][0], round_to_plate_size(scheme[2][1]*float(working_weight), 2.5))]
            })
        return (days, lifts)


class Lift(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class ActiveLift(models.Model):
    ''' Relates Users to the lifts they are currently working on. '''
    user = models.ForeignKey(User, related_name='active_lifts')
    lift = models.ForeignKey(Lift)
    order = models.IntegerField(null=False, blank=False) #the order of this lift in the week
    increment = models.DecimalField(default='5.0', max_digits=4, decimal_places=2)

    def current_pr(self):
        try:
            current_pr = self.lift.prs.filter(user=self.user).order_by('-date')[0]
        except IndexError:
            current_pr = None
        return current_pr

    def get_onerm(self):
        ''' Returns a user's 1RM for this lift. '''
        try:
            onerm = OneRM.objects.filter(user=self.user, lift=self.lift).order_by('-weight')[0]
            return onerm
        except IndexError:
            raise Exception("You must specify a 1RM for this lift") 


class DailyRecord(models.Model):
    '''
    The record of a workout for a given day.

    Should allow us to recreate something like this:

    175x5
    190x5
    205x7

    '''
    user = models.ForeignKey(User, related_name='fto_records')
    date = models.DateTimeField(auto_now_add=True)
    lift = models.ForeignKey(Lift)
    first_set_reps = models.IntegerField()
    first_set_weight = models.DecimalField(max_digits=20, decimal_places=2)
    second_set_reps = models.IntegerField()
    second_set_weight = models.DecimalField(max_digits=20, decimal_places=2)
    third_set_reps = models.IntegerField()
    third_set_weight = models.DecimalField(max_digits=20, decimal_places=2)

    notes = models.CharField(max_length=500, blank=True)



class PR(models.Model):
    date = models.DateField()
    details = models.TextField(blank=True)

    class Meta:
        abstract = True


class LiftPR(PR):
    #These would be a max effort moving of heavy weight
    user = models.ForeignKey(User, related_name='liftprs')
    lift = models.ForeignKey(Lift, related_name='prs')
    reps = models.IntegerField()
    weight = models.DecimalField(max_digits=20, decimal_places=2)#weight in pounds.

    def calc_one_rep_max(self):
        # uses Jim Wendler's calculation for one rep max
        # (weight * reps * .0333) + weight = estimated_total
        if self.reps == 1:#TODO: I should enforce that this not occur
            return self.weight
        else:
            return (float(self.weight) * float(self.reps) * 0.0333) + float(self.weight)


class OneRM(PR):
    user = models.ForeignKey(User, related_name='onerms')
    lift = models.ForeignKey(Lift)
    weight = models.DecimalField(max_digits=20, decimal_places=2)#weight in pounds.
