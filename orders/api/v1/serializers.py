from rest_framework import serializers
from orders.models import Order, OrderItem
from menu.api.v1.serializers import MenuItemSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_details = MenuItemSerializer(source='menu_item', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_details', 'quantity', 'price_at_time', 'notes', 'subtotal']
        read_only_fields = ['price_at_time']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'customer_name', 'order_items', 'status',
            'total_price', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class OrderCreateSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['customer', 'order_items', 'notes']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        
        total_price = 0
        for item_data in order_items_data:
            menu_item = item_data['menu_item']
            quantity = item_data['quantity']
            price_at_time = menu_item.price
            notes = item_data.get('notes', '')
            
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity,
                price_at_time=price_at_time,
                notes=notes
            )
            total_price += price_at_time * quantity
        
        order.total_price = total_price
        order.save()
        return order 