from django.contrib import admin
from rest_framework.permissions import IsAdminUser
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework_nested import routers
from .views import MuseumViewSet, TicketViewSet, EventViewSet, payment_view

router = DefaultRouter()
router.register(r'museums', MuseumViewSet)

museums_router = routers.NestedDefaultRouter(router, r'museums', lookup='museum')
museums_router.register(r'events', EventViewSet, basename='museum-events')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(museums_router.urls)),
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='Darshan Doot API', permission_classes=[IsAdminUser])),
    path('ticket/', TicketViewSet.as_view({'post': 'create'}), name='create_ticket'),
    path('ticket/<uuid:ticket_id>/', TicketViewSet.as_view({'put': 'update', 'delete': 'delete'}), name='ticket_detail'),
    path('ticket/verify/<uuid:ticket_id>/', TicketViewSet.as_view({'post': 'verify'}), name='verify_ticket'),
    path('ticket/payment-verify/<uuid:ticket_id>/', TicketViewSet.as_view({'post': 'payment_verify'}), name='payment_verify'),
    path('payment/<uuid:ticket_id>/', payment_view, name='payment_view'),
]