from django.contrib import admin
from .models import Notification, Occasion

@admin.register(Occasion)
class OccasionAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'recipient_name', 'occasion_type', 'event_date', 'reminder_days_before', 'user')
    list_filter = ('occasion_type', 'event_date')
    search_fields = ('event_title', 'recipient_name', 'user__username')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'notification_type', 'user', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read')
    search_fields = ('title', 'message', 'user__username')
