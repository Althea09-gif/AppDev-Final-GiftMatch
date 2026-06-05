from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)
    favorite_color = models.CharField(max_length=30, default='Pink')
    preferred_budget_min = models.DecimalField(max_digits=10, decimal_places=2, default=500)
    preferred_budget_max = models.DecimalField(max_digits=10, decimal_places=2, default=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name or self.user.username
