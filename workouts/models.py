from django.db import models
from django.contrib.auth.models import User

class Lift(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def current_pr(self):
        return self.prs.order_by('-date')[0]

class PR(models.Model):
    activity = models.CharField(max_length=100)
    date = models.DateField()
    details = models.TextField()

    class Meta:
        abstract = True


class LiftPR(PR):
    #These would be a max effort moving of heavy weight
    user = models.ForeignKey(User, related_name='liftprs')
    lift = models.ForeignKey(Lift, related_name='prs')
    reps = models.IntegerField()
    weight = models.DecimalField(max_digits=20, decimal_places=2)

    def calc_one_rep_max(self):
        # uses Jim Wendler's calculation for one rep max
        # (weight * reps * .0333) + weight = estimated_total
        return (self.weight * self.reps * 0.0333) + self.weight


class TimeWODPR(PR):
    user = models.ForeignKey(User, related_name='timeprs')
    time = models.TimeField()


class AMRAPWODPR(PR):
    user = models.ForeignKey(User, related_name='amrapprs')
    rounds_or_reps = models.DecimalField(max_digits=20, decimal_places=2)
