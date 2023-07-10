from django.db import models

# Create your models here.
class IData(models.Model):
    dd = models.CharField(max_length=255)
    vn = models.CharField(max_length=255)
    ep = models.IntegerField()
    dt = models.JSONField()
