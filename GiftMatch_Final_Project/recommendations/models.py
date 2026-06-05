from django.conf import settings
from django.db import models
from gifts.choices import OCCASION_CHOICES, RECIPIENT_CHOICES


class RecommendationHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendation_history')
    recipient_type = models.CharField(max_length=30, choices=RECIPIENT_CHOICES)
    occasion_type = models.CharField(max_length=30, choices=OCCASION_CHOICES)
    interest_summary = models.CharField(max_length=255, blank=True)
    budget_min = models.DecimalField(max_digits=10, decimal_places=2)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2)
    matched_gifts = models.ManyToManyField('gifts.Gift', blank=True, related_name='recommendation_histories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Recommendations for {self.user.username} on {self.created_at:%Y-%m-%d}'
