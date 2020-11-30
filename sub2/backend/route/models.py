from django.utils import timezone
from django.db import models

class Temp(models.Model):
    temp_id = models.IntegerField(primary_key=True,auto_created=True)
    temp_username=models.CharField(max_length=50, null=True)
    temp_type=models.CharField(max_length=50, null=True)
    temp_typeid=models.IntegerField(null=True)
    temp_title=models.CharField(max_length=200, null=True)
    temp_lat=models.FloatField(max_length=10, null=True)
    temp_lon=models.FloatField(max_length=10, null=True)

