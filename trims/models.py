from django.db import models

class Trim(models.Model):
    name       = models.CharField(max_length = 100)
    front_tire = models.ForeignKey('Tire', on_delete = models.CASCADE, related_name = 'front_tire')
    rear_tire  = models.ForeignKey('Tire', on_delete = models.CASCADE, related_name = 'rear_tire')

    class Meta:
        db_table = 'trims'

class Tire(models.Model):
    width        = models.PositiveIntegerField()
    aspect_ratio = models.PositiveIntegerField()
    wheel_size   = models.PositiveIntegerField()

    class Meta:
        db_table = 'tires'