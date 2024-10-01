from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Museum, Event, Ticket
from django.contrib.auth.models import User
import json
from unittest.mock import patch

class MuseumAPITests(APITestCase):
    def setUp(self):
        self.museum_data = {
            "name": "Test Museum",
            "location": "Test Location",
            "indian_adult_fee": "100.00",
            "indian_child_fee": "50.00",
            "free_for_students": True,
            "camera_fee": "20.00",
            "international_citizen_fee": "500.00",
            "timings": "9 AM - 5 PM",
            "closed_on": "Monday"
        }
        self.museum = Museum.objects.create(**self.museum_data)

    def test_create_museum(self):
        url = reverse('museum-list')
        data = {
            "name": "New Museum",
            "location": "New Location",
            "indian_adult_fee": "150.00",
            "indian_child_fee": "75.00",
            "free_for_students": False,
            "camera_fee": "30.00",
            "international_citizen_fee": "600.00",
            "timings": "10 AM - 6 PM",
            "closed_on": "Tuesday"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Museum.objects.count(), 2)

    def test_get_museums(self):
        url = reverse('museum-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_museum_detail(self):
        url = reverse('museum-detail', kwargs={'pk': self.museum.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.museum_data['name'])

    def test_update_museum(self):
        url = reverse('museum-detail', kwargs={'pk': self.museum.pk})
        updated_data = self.museum_data.copy()
        updated_data['name'] = "Updated Museum Name"
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Museum Name")

class EventAPITests(APITestCase):
    def setUp(self):
        self.museum = Museum.objects.create(name="Test Museum", location="Test Location")
        self.event_data = {
            "name": "Test Event",
            "description": "Test Description",
            "date": "2023-07-01",
            "time_slot": "10 AM - 12 PM",
            "ticket_limit": 100
        }
        self.event = Event.objects.create(museum=self.museum, **self.event_data)

    def test_create_event(self):
        url = reverse('museum-events-list', kwargs={'museum_pk': self.museum.pk})
        data = {
            "name": "New Event",
            "description": "New Description",
            "date": "2023-08-01",
            "time_slot": "2 PM - 4 PM",
            "ticket_limit": 150
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)

    def test_get_events(self):
        url = reverse('museum-events-list', kwargs={'museum_pk': self.museum.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class TicketAPITests(APITestCase):
    def setUp(self):
        self.museum = Museum.objects.create(name="Test Museum", location="Test Location", indian_adult_fee=100, indian_child_fee=50)
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.ticket_data = {
            "user_id": self.user.id,
            "museum": self.museum.id,
            "visiting_date": "2023-07-15",
            "adults": 2,
            "children": 1,
            "people": [
                {"nationality": "Indian", "gender": "Male", "is_indian": True},
                {"nationality": "Indian", "gender": "Female", "is_indian": True},
                {"nationality": "Indian", "gender": "Male", "is_indian": True}
            ]
        }

    @patch('stripe.PaymentIntent.create')
    def test_book_ticket(self, mock_payment_intent):
        mock_payment_intent.return_value = type('obj', (object,), {'client_secret': 'test_client_secret'})
        url = reverse('ticket-book')
        response = self.client.post(url, self.ticket_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('ticket_id', response.data)
        self.assertIn('payment_link', response.data)

    def test_get_ticket_history(self):
        ticket = Ticket.objects.create(user_id=self.user.id, museum=self.museum, visiting_date="2023-07-15", adults=2, children=1, total_amount=250)
        url = reverse('ticket-history', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_latest_ticket(self):
        ticket = Ticket.objects.create(user_id=self.user.id, museum=self.museum, visiting_date="2023-07-15", adults=2, children=1, total_amount=250)
        url = reverse('ticket-latest', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ticket_id'], str(ticket.ticket_id))

    def test_verify_ticket(self):
        ticket = Ticket.objects.create(user_id=self.user.id, museum=self.museum, visiting_date="2023-07-15", adults=2, children=1, total_amount=250)
        url = reverse('ticket-verify')
        data = {"ticket_id": str(ticket.ticket_id), "user_id": self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Ticket verified successfully")

    def test_cancel_ticket(self):
        ticket = Ticket.objects.create(user_id=self.user.id, museum=self.museum, visiting_date="2023-07-15", adults=2, children=1, total_amount=250)
        url = reverse('ticket-cancel')
        data = {"ticket_id": str(ticket.ticket_id), "user_id": self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Ticket cancelled successfully")

class PaymentAPITests(APITestCase):
    def setUp(self):
        self.museum = Museum.objects.create(name="Test Museum", location="Test Location")
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.ticket = Ticket.objects.create(user_id=self.user.id, museum=self.museum, visiting_date="2023-07-15", adults=2, children=1, total_amount=250)

    @patch('stripe.PaymentIntent.create')
    def test_initiate_payment(self, mock_payment_intent):
        mock_payment_intent.return_value = type('obj', (object,), {'client_secret': 'test_client_secret'})
        url = reverse('payments-initiate')
        data = {"ticket_id": str(self.ticket.ticket_id), "amount": 250}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('payment_link', response.data)

    @patch('stripe.PaymentIntent.retrieve')
    def test_confirm_payment(self, mock_payment_intent):
        mock_payment_intent.return_value = type('obj', (object,), {'status': 'succeeded'})
        url = reverse('payments-confirm')
        data = {"ticket_id": str(self.ticket.ticket_id), "transaction_id": "test_transaction_id"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Payment confirmed successfully")