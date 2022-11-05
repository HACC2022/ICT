from django.contrib import admin
from .models import Url, IP_Adresses

# Register your models here.
admin.site.register(Url)
admin.site.register(IP_Adresses)