from django.contrib import admin
from .models import WishlistItem

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'gift', 'purchased', 'created_at')
    list_filter = ('purchased',)
    search_fields = ('user__username', 'gift__name')
