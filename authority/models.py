from django.db import models
from django.conf import settings
from .choices import *

class AlgoDetails(models.Model):
    resourceType = models.CharField(max_length=200, choices=type_choices)
    resourceTitle = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    algorithmUsed = models.CharField(max_length=200, choices=algorithms_choices)
    techniqueUsed = models.CharField(max_length=200)
    techniqueDescription = models.CharField(max_length=200)
    document = models.FileField(upload_to='res/')
    requestStatus = models.CharField(max_length=200, default='admin')
    userId = models.IntegerField(default=0)