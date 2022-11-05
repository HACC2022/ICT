from django.db import models
from datetime import date

# Create your models here.
class Url(models.Model):
    longLink = models.CharField(max_length=1000)
    shortCode = models.CharField(max_length=30)
    creationDate = models.DateField(default=date.today)
    clicks = models.IntegerField(default=0)

class IP_Adresses(models.Model):
    shortCode = models.ForeignKey(Url, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(default='192.168.0.1')