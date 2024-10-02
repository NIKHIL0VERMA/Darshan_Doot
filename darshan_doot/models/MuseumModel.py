from django.db import models

class Museum(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    indian_adult_fee = models.DecimalField(max_digits=10, decimal_places=2)
    indian_child_fee = models.DecimalField(max_digits=10, decimal_places=2)
    free_for_students = models.BooleanField(default=False)
    camera_fee = models.DecimalField(max_digits=10, decimal_places=2)
    international_citizen_fee = models.DecimalField(max_digits=10, decimal_places=2)
    timings = models.CharField(max_length=255)
    closed_on = models.CharField(max_length=255)