from rest_framework import serializers
from reservations.models import Table, Reservation

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'number', 'capacity', 'is_available', 'location', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ReservationSerializer(serializers.ModelSerializer):
    table_details = TableSerializer(source='table', read_only=True)
    customer_name = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id', 'customer', 'customer_name', 'table', 'table_details',
            'date', 'time', 'number_of_guests', 'status', 'special_requests',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        if data.get('number_of_guests') and data.get('table'):
            if data['number_of_guests'] > data['table'].capacity:
                raise serializers.ValidationError("Number of guests exceeds table capacity")
        return data 