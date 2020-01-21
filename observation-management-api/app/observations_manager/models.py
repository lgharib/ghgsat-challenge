from django.contrib.gis.db import models


class Target(models.Model):
    name = models.CharField(max_length=50)
    coordinates = models.PointField(null=True, blank=True)
    elevation = models.IntegerField()

    def __str__(self):
        return self.name
