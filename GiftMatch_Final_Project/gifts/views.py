from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .forms import GiftFinderForm
from .models import Gift, Interest
from .services import marketplace_urls_for_gift
from occasions.models import Occasion


def _infer_recipient_type(occasion):
    occasion_type = occasion.occasion_type
    name = (occasion.recipient_name or '').lower()
    title = (occasion.event_title or '').lower()
    family_words = ['mom', 'mother', 'mama', 'dad', 'father', 'papa', 'sister', 'brother', 'family', 'lola', 'lolo', 'aunt', 'uncle']
    partner_words = ['wife', 'husband', 'girlfriend', 'boyfriend', 'partner', 'anniversary', 'monthsary']
    coworker_words = ['boss', 'manager', 'coworker', 'colleague', 'workmate']
    combined = f'{name} {title}'
    if occasion_type in ['mothers_day', 'fathers_day', 'family_reunion'] or any(word in combined for word in family_words):
        return 'family'
    if occasion_type in ['anniversary', 'valentines', 'monthsary'] or any(word in combined for word in partner_words):
        return 'partner'
    if occasion_type in ['promotion', 'retirement'] or any(word in combined for word in coworker_words):
        return 'coworker'
    return 'friend'


@login_required
def finder(request):
    initial = {}
    selected_interest_ids = set()
    prefilled_recipient_name = ''

    occasion_id = request.GET.get('occasion_id')
    if occasion_id:
        try:
            occasion = Occasion.objects.get(pk=occasion_id, user=request.user)
            initial.update({
                'recipient_type': _infer_recipient_type(occasion),
                'occasion_type': occasion.occasion_type,
                'recipient_name': occasion.recipient_name,
            })
            prefilled_recipient_name = occasion.recipient_name
        except Occasion.DoesNotExist:
            pass

    if request.GET.get('recipient_type'):
        initial['recipient_type'] = request.GET.get('recipient_type')
    if request.GET.get('occasion_type'):
        initial['occasion_type'] = request.GET.get('occasion_type')
    if request.GET.get('budget_range'):
        initial['budget_range'] = request.GET.get('budget_range')
    if request.GET.get('marketplace'):
        initial['marketplace'] = request.GET.get('marketplace')
    if request.GET.get('recipient_name'):
        initial['recipient_name'] = request.GET.get('recipient_name')
        prefilled_recipient_name = request.GET.get('recipient_name')

    interests_from_query = request.GET.getlist('interests')
    if interests_from_query:
        selected_interest_ids = {int(value) for value in interests_from_query if value.isdigit()}
        initial['interests'] = list(Interest.objects.filter(id__in=selected_interest_ids))

    form = GiftFinderForm(initial=initial)
    featured = Gift.objects.filter(is_featured=True).select_related('category').prefetch_related('interests')[:3]
    return render(request, 'gifts/finder.html', {
        'form': form,
        'featured': featured,
        'selected_recipient_type': initial.get('recipient_type', 'partner'),
        'selected_occasion_type': initial.get('occasion_type', 'anniversary'),
        'selected_budget_range': initial.get('budget_range', '500-1500'),
        'selected_marketplace': initial.get('marketplace', 'any'),
        'selected_interest_ids': selected_interest_ids,
        'prefilled_recipient_name': prefilled_recipient_name,
    })


@login_required
def detail(request, pk):
    gift = get_object_or_404(Gift.objects.select_related('category').prefetch_related('interests'), pk=pk)
    related = Gift.objects.filter(category=gift.category).exclude(pk=gift.pk)[:3]
    marketplace_urls = marketplace_urls_for_gift(gift.name)
    back_url = request.META.get('HTTP_REFERER') or reverse('gifts:finder')
    return render(request, 'gifts/detail.html', {
        'gift': gift,
        'related': related,
        'marketplace_urls': marketplace_urls,
        'back_url': back_url,
    })
