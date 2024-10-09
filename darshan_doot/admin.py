from django.contrib import admin
from django.db.models import Sum
from .models import Event, Museum, Ticket

@admin.register(Museum)
class MuseumAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'indian_adult_fee', 'international_citizen_fee', 'timings', 'closed_on')
    search_fields = ('name', 'location')
    ordering = ('name',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        'ticket_id',
        'user_phone',
        'museum',
        'visiting_date',
        'payment_status',
        'booking_date',
    ]
    
    list_filter = ['payment_status', 'museum']
    search_fields = ('user_phone', 'ticket_id', 'transaction_id')
    date_hierarchy = 'visiting_date'

    def total_persons(self, obj):
        return obj.adults + obj.children

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _total_persons=Sum('adults') + Sum('children')
        )
        return queryset

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'total_sales': qs.aggregate(total_sales=Sum('total_amount'))['total_sales'],
            'total_tickets': qs.count(),
            'total_persons': qs.aggregate(total_persons=Sum('adults') + Sum('children'))['total_persons'],
        }
        
        response.context_data['summary'] = metrics
        return response

    def has_add_permission(self, request):
        return False  # Prevent adding tickets directly from admin

    def has_change_permission(self, request, obj=None):
        return False  # Prevent changing tickets directly from admin

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deleting tickets directly from admin

    def user_nationality(self, obj):
        return obj.user.nationality if obj.user else None
    user_nationality.short_description = 'Nationality'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'description')  # Customize the display fields
