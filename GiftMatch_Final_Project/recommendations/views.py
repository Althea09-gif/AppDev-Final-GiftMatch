from urllib.parse import urlencode
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from gifts.forms import GiftFinderForm
from gifts.services import fetch_external_products
from .engine import score_gifts
from .models import RecommendationHistory


@login_required
def results(request):
    if request.method != 'POST':
        return redirect('gifts:finder')
    form = GiftFinderForm(request.POST)
    if not form.is_valid():
        messages.error(request, 'Please complete the gift finder form and select at least one interest.')
        return redirect('gifts:finder')

    recipient_type = form.cleaned_data['recipient_type']
    occasion_type = form.cleaned_data['occasion_type']
    recipient_name = form.cleaned_data.get('recipient_name', '')
    interests = list(form.cleaned_data['interests'])
    budget_min, budget_max = form.budget_min_max()
    budget_range = form.cleaned_data['budget_range']
    marketplace = form.cleaned_data.get('marketplace') or 'any'
    scored = score_gifts(recipient_type, occasion_type, interests, budget_min, budget_max, marketplace)

    history = RecommendationHistory.objects.create(
        user=request.user,
        recipient_type=recipient_type,
        occasion_type=occasion_type,
        interest_summary=', '.join([i.name for i in interests]),
        budget_min=budget_min,
        budget_max=budget_max,
    )
    history.matched_gifts.set([item['gift'] for item in scored[:24]])

    keyword = interests[0].name if interests else 'gift'
    external_products = fetch_external_products(keyword, budget_min, budget_max, limit=8, marketplace=marketplace)
    query_pairs = [
        ('recipient_type', recipient_type),
        ('occasion_type', occasion_type),
        ('budget_range', budget_range),
        ('marketplace', marketplace),
        ('recipient_name', recipient_name),
    ]
    query_pairs.extend(('interests', str(interest.id)) for interest in interests)
    edit_search_url = f"/gifts/finder/?{urlencode(query_pairs)}"

    return render(request, 'recommendations/results.html', {
        'form': form,
        'scored': scored[:24],
        'external_products': external_products,
        'history': history,
        'recipient_type': recipient_type,
        'occasion_type': occasion_type,
        'recipient_name': recipient_name,
        'interests': interests,
        'budget_min': budget_min,
        'budget_max': budget_max,
        'budget_range': budget_range,
        'marketplace': marketplace,
        'edit_search_url': edit_search_url,
    })
