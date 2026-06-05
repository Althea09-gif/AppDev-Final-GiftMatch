from django.conf import settings
from django.db import models


class WishlistItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist_items')
    gift = models.ForeignKey('gifts.Gift', on_delete=models.CASCADE, related_name='wishlist_items')
    purchased = models.BooleanField(default=False)
    notes = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'gift')
        ordering = ['purchased', '-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.gift.name}'
