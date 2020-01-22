from django.contrib.gis.db import models


class Target(models.Model):
    name = models.CharField(max_length=50)
    coordinates = models.PointField(null=True, blank=True)
    elevation = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class Observation(models.Model):
    target = models.ForeignKey(Target, related_name='observations',
                               on_delete=models.CASCADE, null=True)
    image_url = models.URLField(max_length=1000)
    timestamp = models.DateTimeField()

    def __str__(self):
        return str(self.image_url)

    class Meta:
        ordering = ['-id']
