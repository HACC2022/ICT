from django.db import models

# Create your models here.
class Url(models.Model):
    longLink = models.CharField(max_length=50)
    shortCode = models.CharField(max_length=30)
    user = models.CharField(max_length=30)