from django.db import models
import uuid
from django.core.validators import EmailValidator

class Ticket(models.Model):
    ticket_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_phone = models.CharField(max_length=15)  # User's phone number
    user_email = models.EmailField(validators=[EmailValidator()], max_length=254)  # User's email
    museum = models.ForeignKey('Museum', on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    visiting_date = models.DateField()
    payment_status = models.CharField(max_length=20, default='pending')
    adults = models.PositiveIntegerField()
    children = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    verification_code = models.CharField(max_length=20, blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    nationality = models.CharField(max_length=100) 

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

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    description = models.TextField()

