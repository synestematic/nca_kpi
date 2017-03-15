from django.db import models

class Day(models.Model):
    date = models.DateTimeField()
    incomingCalls = models.IntegerField()
    answeredCalls = models.IntegerField()
    lessThan20Secs = models.IntegerField()
    unansweredCalls = models.IntegerField()

    #firstContactResolution
    #satisfactionLevel

    averageCallTime = models.DecimalField(decimal_places=1, max_digits=3)
    averageQueueTime = models.DecimalField(decimal_places=1, max_digits=3)

    #transferedCalls
    #utlizationPercentage
    #occupationPercentage
