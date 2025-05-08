from django.contrib import admin
from .models import Feedback, FeedbackImage

class FeedbackImageInline(admin.TabularInline):
    model = FeedbackImage
    extra = 1

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'rating', 'order', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('customer__username', 'comment', 'staff_response')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [FeedbackImageInline]
    list_editable = ('rating',)

@admin.register(FeedbackImage)
class FeedbackImageAdmin(admin.ModelAdmin):
    list_display = ('feedback', 'image', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('feedback__customer__username',)
    readonly_fields = ('created_at',)
