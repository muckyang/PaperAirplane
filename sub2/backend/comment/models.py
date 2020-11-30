from django.db import models

# Create your models here.
class Comment(models.Model):
    id = models.IntegerField(primary_key=True,auto_created=True)
    userid = models.IntegerField(null=True)
    storeid = models.IntegerField(null=True)
    tourspotid = models.IntegerField(null=True)
    description = models.TextField(null=True)
    score = models.FloatField(null=True)