from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'favorite_color', 'preferred_budget_min', 'preferred_budget_max')
    search_fields = ('user__username', 'full_name', 'user__email')
