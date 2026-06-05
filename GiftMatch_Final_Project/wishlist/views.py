from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from gifts.models import Gift
from occasions.models import Notification
from .models import WishlistItem


@login_required
def wishlist_list(request):
    items = WishlistItem.objects.filter(user=request.user).select_related('gift', 'gift__category')
    return render(request, 'wishlist/list.html', {'items': items})


@login_required
@require_POST
def add_to_wishlist(request, gift_id):
    gift = get_object_or_404(Gift, pk=gift_id)
    item, created = WishlistItem.objects.get_or_create(user=request.user, gift=gift)
    if created:
        Notification.objects.create(
            user=request.user,
            notification_type='wishlist',
            title='Gift saved to wishlist',
            message=f'{gift.name} was added to your wishlist.',
            gift=gift,
        )
        messages.success(request, 'Gift added to wishlist.')
    else:
        messages.info(request, 'This gift is already in your wishlist.')
    return redirect(request.POST.get('next') or 'wishlist:list')


@login_required
@require_POST
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(WishlistItem, pk=item_id, user=request.user)
    item.delete()
    messages.info(request, 'Gift removed from wishlist.')
    return redirect('wishlist:list')


@login_required
@require_POST
def toggle_purchased(request, item_id):
    item = get_object_or_404(WishlistItem, pk=item_id, user=request.user)
    item.purchased = not item.purchased
    item.save()
    status_text = 'purchased' if item.purchased else 'planning to buy'
    Notification.objects.create(
        user=request.user,
        notification_type='wishlist',
        title='Wishlist item marked as purchased' if item.purchased else 'Wishlist status updated',
        message=f'{item.gift.name} is now marked as {status_text}.',
        gift=item.gift,
    )
    messages.success(request, 'Wishlist item updated.')
    return redirect('wishlist:list')
