from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from gifts.models import Gift
from .forms import OccasionForm
from .models import Notification, Occasion


@login_required
def occasion_list(request):
    form = OccasionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        occasion = form.save(commit=False)
        occasion.user = request.user
        occasion.save()
        Notification.objects.create(
            user=request.user,
            notification_type='occasion',
            title='New occasion saved',
            message=f"Reminder set for {occasion.event_title} on {occasion.event_date}.",
            occasion=occasion,
        )
        messages.success(request, 'Occasion saved successfully.')
        return redirect('occasions:list')
    occasions = Occasion.objects.filter(user=request.user).order_by('event_date')
    return render(request, 'occasions/list.html', {'form': form, 'occasions': occasions, 'today': timezone.localdate()})


@login_required
def occasion_edit(request, pk):
    occasion = get_object_or_404(Occasion, pk=pk, user=request.user)
    form = OccasionForm(request.POST or None, instance=occasion)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Occasion updated.')
        return redirect('occasions:list')
    return render(request, 'occasions/form.html', {'form': form, 'occasion': occasion})


@login_required
def occasion_delete(request, pk):
    occasion = get_object_or_404(Occasion, pk=pk, user=request.user)
    if request.method == 'POST':
        occasion.delete()
        messages.info(request, 'Occasion deleted.')
        return redirect('occasions:list')
    return render(request, 'occasions/confirm_delete.html', {'occasion': occasion})


@login_required
def notification_list(request):
    today = timezone.localdate()
    upcoming = Occasion.objects.filter(user=request.user, event_date__gte=today).order_by('event_date')[:5]
    recent_gifts = Gift.objects.order_by('-created_at')[:4]
    notifications = Notification.objects.filter(user=request.user).select_related('occasion', 'gift')[:20]
    return render(request, 'occasions/notifications.html', {
        'upcoming': upcoming,
        'recent_gifts': recent_gifts,
        'notifications': notifications,
    })


@login_required
def notification_mark_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save(update_fields=['is_read'])
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'notifications:list'
    return redirect(next_url)


@login_required
def notification_clear_all(request):
    Notification.objects.filter(user=request.user).delete()
    messages.success(request, 'Notifications cleared.')
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'notifications:list'
    return redirect(next_url)
