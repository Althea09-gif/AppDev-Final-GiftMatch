from django.contrib import admin
from .models import RecommendationHistory

@admin.register(RecommendationHistory)
class RecommendationHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipient_type', 'occasion_type', 'budget_min', 'budget_max', 'created_at')
    list_filter = ('recipient_type', 'occasion_type')
    search_fields = ('user__username', 'interest_summary')
    filter_horizontal = ('matched_gifts',)
