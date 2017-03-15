from django.db import models

class Item(models.Model):
    tag = models.IntegerField()
    device = models.CharField(max_length=100)
    history = models.TextField()
    accountedFor = models.BooleanField()
