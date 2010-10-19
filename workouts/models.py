from django.db import models
from django.contrib.auth.models import User

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


class PR(models.Model):
    date = models.DateField()
    details = models.TextField()

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


class TimeWODPR(PR):
    user = models.ForeignKey(User, related_name='timeprs')
    workout = models.CharField(max_length=100)
    time = models.TimeField()


class AMRAPWODPR(PR):
    user = models.ForeignKey(User, related_name='amrapprs')
    rounds_or_reps = models.DecimalField(max_digits=20, decimal_places=2)
