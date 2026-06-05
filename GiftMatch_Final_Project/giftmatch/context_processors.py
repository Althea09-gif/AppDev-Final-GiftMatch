def global_counts(request):
    if not request.user.is_authenticated:
        return {}
    try:
        from wishlist.models import WishlistItem
        from occasions.models import Occasion, Notification
        unread = Notification.objects.filter(user=request.user, is_read=False).count()
        return {
            'wishlist_count': WishlistItem.objects.filter(user=request.user, purchased=False).count(),
            'occasion_count': Occasion.objects.filter(user=request.user).count(),
            'notification_count': unread,
            'nav_notifications': Notification.objects.filter(user=request.user).select_related('gift', 'occasion').order_by('-created_at')[:6],
        }
    except Exception:
        return {}
