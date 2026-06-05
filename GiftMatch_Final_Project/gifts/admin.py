from django.contrib import admin
from .models import Category, Gift, Interest

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'recipient_type', 'occasion_type', 'price', 'store_name', 'is_featured')
    list_filter = ('recipient_type', 'occasion_type', 'store_name', 'category', 'is_featured')
    search_fields = ('name', 'description')
    filter_horizontal = ('interests',)
