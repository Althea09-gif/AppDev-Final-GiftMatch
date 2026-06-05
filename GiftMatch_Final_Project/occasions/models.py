from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone
from gifts.choices import OCCASION_CHOICES


class Occasion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='occasions')
    event_title = models.CharField(max_length=160)
    recipient_name = models.CharField(max_length=120)
    occasion_type = models.CharField(max_length=30, choices=OCCASION_CHOICES)
    event_date = models.DateField()
    reminder_days_before = models.PositiveIntegerField(default=7)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['event_date']

    def __str__(self):
        return f'{self.event_title} for {self.recipient_name}'

    @property
    def days_left(self):
        return (self.event_date - timezone.localdate()).days

    @property
    def reminder_date(self):
        return self.event_date - timedelta(days=self.reminder_days_before)

    @property
    def is_upcoming(self):
        return self.event_date >= timezone.localdate()


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('occasion', 'Occasion Reminder'),
        ('wishlist', 'Wishlist Update'),
        ('recommendation', 'Gift Suggestion'),
        ('system', 'System Message'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES, default='system')
    title = models.CharField(max_length=160)
    message = models.TextField()
    occasion = models.ForeignKey(Occasion, on_delete=models.SET_NULL, null=True, blank=True)
    gift = models.ForeignKey('gifts.Gift', on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
