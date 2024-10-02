from rest_framework import serializers
from .models import EventModel, Museum, Ticket

class MuseumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Museum
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventModel
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ('ticket_id', 'booking_date', 'payment_status', 'total_amount', 'transaction_id', 'verification_code', 'stripe_payment_intent_id')

    def create(self, validated_data):
        ticket = Ticket.objects.create(**validated_data)
        return ticket
