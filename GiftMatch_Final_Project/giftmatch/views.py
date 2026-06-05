from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

from gifts.models import Gift
from occasions.models import Occasion, Notification
from wishlist.models import WishlistItem


def landing(request):
    featured = Gift.objects.select_related('category').all()[:3]
    return render(request, 'landing.html', {'featured_gifts': featured})


@login_required
def dashboard(request):
    today = timezone.localdate()
    next_month = today + timedelta(days=30)
    upcoming = Occasion.objects.filter(user=request.user, event_date__gte=today, event_date__lte=next_month).order_by('event_date')[:4]
    wishlist_items = WishlistItem.objects.filter(user=request.user).select_related('gift')[:3]
    curated = Gift.objects.select_related('category').prefetch_related('interests').all()[:6]
    notifications = Notification.objects.filter(user=request.user).select_related('gift', 'occasion').order_by('-created_at')[:4]
    return render(request, 'dashboard.html', {
        'upcoming': upcoming,
        'wishlist_items': wishlist_items,
        'curated': curated,
        'notifications': notifications,
    })


@login_required
def pro(request):
    return render(request, 'pages/pro.html')


def offline(request):
    return render(request, 'offline.html')


def about(request):
    return render(request, 'pages/about.html')


def privacy(request):
    return render(request, 'pages/privacy.html')


def terms(request):
    return render(request, 'pages/terms.html')


def contact(request):
    return render(request, 'pages/contact.html')
