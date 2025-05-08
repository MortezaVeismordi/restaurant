from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from reservations.models import Table, Reservation
from .serializers import TableSerializer, ReservationSerializer

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['is_available', 'capacity']
    search_fields = ['location']
    ordering_fields = ['number', 'capacity']

    @action(detail=False, methods=['get'])
    def available(self, request):
        date = request.query_params.get('date')
        time = request.query_params.get('time')
        
        if not date or not time:
            return Response(
                {"error": "Both date and time are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get all tables that are not reserved for the given date and time
        reserved_tables = Reservation.objects.filter(
            date=date,
            time=time,
            status__in=['pending', 'confirmed']
        ).values_list('table_id', flat=True)

        available_tables = self.queryset.exclude(id__in=reserved_tables)
        serializer = self.get_serializer(available_tables, many=True)
        return Response(serializer.data)

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'date', 'table']
    search_fields = ['customer__username', 'customer__email']
    ordering_fields = ['date', 'time', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(customer=user)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        if not request.user.is_staff:
            return Response(
                {"error": "Only staff members can update reservation status"},
                status=status.HTTP_403_FORBIDDEN
            )

        reservation = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Reservation.STATUS_CHOICES):
            return Response(
                {"error": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST
            )

        reservation.status = new_status
        reservation.save()
        serializer = self.get_serializer(reservation)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        today = timezone.now().date()
        upcoming_reservations = self.get_queryset().filter(date__gte=today)
        serializer = self.get_serializer(upcoming_reservations, many=True)
        return Response(serializer.data) 