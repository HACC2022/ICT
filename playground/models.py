from django.db import models
from datetime import date

# Create your models here.
class Url(models.Model):
    longLink = models.CharField(max_length=1000)
    shortCode = models.CharField(max_length=30)