from django.db import models
from django.utils import timezone
from datetime import date

class Stats(models.Model):
    # id = models.AutoField(default=1, primary_key=True)
    # date = models.DateField(default=date.today(), primary_key=True)
    date = models.DateField(default=timezone.now, primary_key=True)
    incoming_calls = models.IntegerField(default=0)
    unanswered_calls = models.IntegerField(default=0)
    answered_calls = models.IntegerField(default=0)
    fast_calls = models.IntegerField(default=0)

    total_connection_time = models.IntegerField(default=0)
    total_wait_time = models.IntegerField(default=0)
    average_connection_time = models.DecimalField(decimal_places=1, max_digits=6, default=0.0)
    average_wait_time = models.DecimalField(decimal_places=1, max_digits=6, default=0.0)

    class Meta:
        abstract = True # abstract classes only serve as models for subclasses and do not generate their own db table

class Stats_ops(Stats):
    department = models.CharField(default='ops',max_length=20)
    ivr_average_duration = models.IntegerField(default=15)

    # subsets of unanswered calls
    abandoned_soon_calls = models.IntegerField(default=0)
    satisfied_calls = models.IntegerField(default=0)


class Stats_bc(Stats):
    department = models.CharField(default='bc',max_length=20)
    ivr_average_duration = models.IntegerField(default=80)
