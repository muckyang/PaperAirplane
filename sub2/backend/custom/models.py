from django.db import models

# Create your models here.
class Custom(models.Model):
    id = models.IntegerField(primary_key=True,auto_created=True)
    userid = models.IntegerField()
    orderid = models.IntegerField(null=True)
    order = models.IntegerField(null=True)
    contenttype = models.IntegerField(null=True)
    contentid = models.IntegerField(null=True)
    latitude = models.FloatField(max_length=20, null=True)
    longitude = models.FloatField(max_length=20, null=True)