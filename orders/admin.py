from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('subtotal',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__username', 'customer__email', 'id')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]
    list_editable = ('status',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity', 'price_at_time', 'subtotal')
    list_filter = ('order__status',)
    search_fields = ('order__id', 'menu_item__name')
    readonly_fields = ('subtotal',)
