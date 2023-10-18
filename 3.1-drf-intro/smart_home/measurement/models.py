from django.db import models


class Sensor(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)


class Measurement(models.Model):
    sensor_id = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    temperature = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
