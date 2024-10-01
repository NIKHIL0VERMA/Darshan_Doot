from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Museum, Ticket, Event
from .serializers import MuseumSerializer, TicketSerializer, EventSerializer
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import stripe
from django.db import transaction
from datetime import datetime
import pytz
from django.shortcuts import render

stripe.api_key = settings.STRIPE_SECRET_KEY

class MuseumViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing and editing museum instances.
    """
    queryset = Museum.objects.all()
    serializer_class = MuseumSerializer

    def list(self, request):
        """
        List all museums or filter by name and location.
        Query Parameters:
            - name: Filter museums by name (case-insensitive).
            - location: Filter museums by location (case-insensitive).
        Returns:
            A list of museums matching the filters.
        """
        name = request.query_params.get('name', None)
        location = request.query_params.get('location', None)
        queryset = self.get_queryset()

        if name:
            queryset = queryset.filter(name__icontains=name)
        if location:
            queryset = queryset.filter(location__icontains=location)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class TicketViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing ticket instances.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def create(self, request):
        """
        Create a new ticket.
        Request Body:
            - user_phone: User's phone number.
            - user_email: User's email.
            - adults: Number of adults.
            - children: Number of children.
            - visiting_date: Date of the visit.
            - museum_name: Name of the museum.
            - nationality: User's nationality.
        """
        required_fields = ['user_phone', 'user_email', 'adults', 'children', 'visiting_date', 'museum_name', 'nationality']
        
        # Check for missing required fields
        for field in required_fields:
            if field not in request.data:
                return Response({'error': f'Missing required field: {field}'}, status=status.HTTP_400_BAD_REQUEST)

        user_phone = request.data['user_phone']
        user_email = request.data['user_email']
        adults = request.data['adults']
        children = request.data['children']
        visiting_date = request.data['visiting_date']
        museum_name = request.data['museum_name']
        nationality = request.data['nationality']

        # Check if the museum is open on the visiting date
        museum = Museum.objects.filter(name=museum_name).first()
        if not museum:
            return Response({'error': 'Museum not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the visiting date is a holiday
        visiting_date_obj = datetime.strptime(visiting_date, '%Y-%m-%d').date()
        if visiting_date_obj.weekday() in [5, 6]:  # Saturday=5, Sunday=6
            return Response({'error': 'Museum is closed on weekends.'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total amount based on nationality
        if nationality.lower() == 'indian':
            total_amount = (museum.indian_adult_fee * adults) + (museum.indian_child_fee * children)
        else:
            total_amount = (museum.international_citizen_fee * adults) + (museum.international_citizen_fee * children)

        # Create the ticket
        ticket = Ticket(
            user_phone=user_phone,
            user_email=user_email,
            museum=museum,
            visiting_date=visiting_date_obj,
            adults=adults,
            children=children,
            total_amount=total_amount,
            payment_status='pending',
            booking_date=timezone.now(),
            nationality=nationality
        )

        with transaction.atomic():
            ticket.save()

        # Generate Stripe payment intent URL
        ticket.stripe_payment_intent_id = f"/payment/{ticket.ticket_id}/"
        ticket.save()

        response_data = {
            'ticket_id': ticket.ticket_id,
            'user_phone': user_phone,
            'user_email': user_email,
            'adults': adults,
            'children': children,
            'visiting_date': visiting_date,
            'museum_name': museum.name,
            'total_amount': total_amount,
            'stripe_payment_intent': ticket.stripe_payment_intent_id
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    def update(self, request, ticket_id):
        """
        Update a ticket.
        """
        try:
            ticket = Ticket.objects.get(ticket_id=ticket_id)
            # Update fields as necessary
            # Example: ticket.user_phone = request.data.get('user_phone')
            ticket.save()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({'status': 'not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, ticket_id):
        """
        Delete a ticket.
        """
        try:
            ticket = Ticket.objects.get(ticket_id=ticket_id)
            ticket.delete()
            return Response({'status': 'success'}, status=status.HTTP_204_NO_CONTENT)
        except Ticket.DoesNotExist:
            return Response({'status': 'not found'}, status=status.HTTP_404_NOT_FOUND)

    def verify(self, request, ticket_id):
        """
        Verify a ticket using ticket_id and verification_code.
        """
        verification_code = request.data.get('verification_code')
        try:
            ticket = Ticket.objects.get(ticket_id=ticket_id, verification_code=verification_code)
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({'status': 'not found'}, status=status.HTTP_404_NOT_FOUND)

    def payment_verify(self, request, ticket_id):
        """
        Verify payment using ticket_id and transaction_id.
        """
        transaction_id = request.data.get('transaction_id')
        try:
            ticket = Ticket.objects.get(ticket_id=ticket_id, transaction_id=transaction_id)
            ticket.payment_status = 'paid'
            ticket.verification_code = 'generated_verification_code'  # Generate a unique verification code
            ticket.transaction_id = transaction_id
            ticket.save()
            return Response({
                'ticket_id': ticket.ticket_id,
                'verification_code': ticket.verification_code,
                'payment_status': ticket.payment_status,
                'amount': ticket.total_amount,
                'adults': ticket.adults,
                'children': ticket.children
            }, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({'status': 'not found'}, status=status.HTTP_404_NOT_FOUND)

class EventViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing event instances.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def list(self, request):
        """
        List all events.
        Returns:
            A list of all events.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new event.
        Request Body:
            - name: The name of the event.
            - date: The date and time of the event.
            - description: A description of the event.
        Returns:
            The created event data.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def stripe_webhook(request):
    """
    Handle Stripe webhook events.
    This function processes events sent by Stripe, such as payment confirmations and cancellations.
    Returns:
        HTTP response indicating the status of the event handling.
    """
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        ticket_id = payment_intent.metadata.get('ticket_id')
        if ticket_id:
            ticket = Ticket.objects.get(ticket_id=ticket_id)
            ticket.payment_status = 'paid'
            ticket.save()
    elif event.type == 'payment_intent.canceled':
        payment_intent = event.data.object
        ticket_id = payment_intent.metadata.get('ticket_id')
        if ticket_id:
            ticket = Ticket.objects.get(ticket_id=ticket_id)
            ticket.payment_status = 'cancelled'
            ticket.save()
    elif event.type == 'charge.refunded':
        charge = event.data.object
        ticket_id = charge.metadata.get('ticket_id')
        if ticket_id:
            ticket = Ticket.objects.get(ticket_id=ticket_id)
            ticket.payment_status = 'refunded'
            ticket.save()

    return HttpResponse(status=200)

def payment_view(request, ticket_id):
    """
    Render the payment details for a specific ticket.
    """
    try:
        ticket = Ticket.objects.get(ticket_id=ticket_id)
        context = {
            'museum_name': ticket.museum.name,
            'visiting_date': ticket.visiting_date,
            'total_amount': ticket.total_amount,
            'adults': ticket.adults,
            'children': ticket.children,
            'ticket_id': ticket.ticket_id,
            'payment_status': ticket.payment_status,
        }
        return render(request, 'payment_details.html', context)
    except Ticket.DoesNotExist:
        return Response({'error': 'Ticket not found.'}, status=status.HTTP_404_NOT_FOUND)