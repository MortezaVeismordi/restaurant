from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from orders.models import Order

class Feedback(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedbacks')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedbacks')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5"
    )
    comment = models.TextField()
    staff_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback from {self.customer.username} - Rating: {self.rating}"

class FeedbackImage(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='feedback_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Feedback #{self.feedback.id}"
