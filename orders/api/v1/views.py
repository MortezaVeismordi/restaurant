from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from orders.models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer, OrderItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'customer']
    search_fields = ['customer__username', 'customer__email']
    ordering_fields = ['created_at', 'total_price']

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer=user)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        if not request.user.is_staff:
            return Response(
                {"error": "Only staff members can update order status"},
                status=status.HTTP_403_FORBIDDEN
            )

        order = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {"error": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['order']
    search_fields = ['menu_item__name']
    ordering_fields = ['quantity', 'price_at_time'] 