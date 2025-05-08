from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    is_available = models.BooleanField(default=True)
    location = models.CharField(max_length=100, blank=True)  # e.g., "Window", "Bar", "Outdoor"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Table {self.number} (Capacity: {self.capacity})"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']
        unique_together = ['table', 'date', 'time']

    def __str__(self):
        return f"Reservation #{self.id} - {self.customer.username} on {self.date} at {self.time}"

    def clean(self):
        if self.number_of_guests > self.table.capacity:
            raise models.ValidationError("Number of guests exceeds table capacity")
