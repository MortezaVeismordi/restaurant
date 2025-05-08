from django.contrib import admin
from .models import Table, Reservation

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'is_available', 'location')
    list_filter = ('is_available', 'capacity')
    search_fields = ('number', 'location')
    list_editable = ('is_available', 'capacity')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'table', 'date', 'time', 'number_of_guests', 'status')
    list_filter = ('status', 'date', 'table')
    search_fields = ('customer__username', 'customer__email', 'id')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)
    date_hierarchy = 'date'
