from gifts.models import Gift


def _display_list(items):
    names = [str(item.name if hasattr(item, 'name') else item) for item in items]
    if not names:
        return ''
    if len(names) == 1:
        return names[0]
    return ', '.join(names[:-1]) + ' and ' + names[-1]


def score_gifts(recipient_type, occasion_type, interests, budget_min, budget_max, marketplace='any'):
    """Strict, explainable recommendation engine.

    Rules:
    1. Recipient and occasion must match.
    2. Price must stay inside the selected budget range.
    3. If interests are selected, gifts must share at least one selected interest.
    4. Marketplace is filtered when the user chooses a specific store.
    """
    selected_interest_ids = {interest.id for interest in interests}
    selected_interest_names = _display_list(interests)

    qs = Gift.objects.select_related('category').prefetch_related('interests').filter(
        recipient_type=recipient_type,
        occasion_type=occasion_type,
        price__gte=budget_min,
        price__lte=budget_max,
    )
    if marketplace and marketplace != 'any':
        qs = qs.filter(store_name=marketplace)

    results = []
    seen_names = set()
    for gift in qs:
        if not marketplace or marketplace == 'any':
            if gift.name in seen_names:
                continue
            seen_names.add(gift.name)
        gift_interest_ids = set(gift.interests.values_list('id', flat=True))
        shared_ids = selected_interest_ids.intersection(gift_interest_ids)
        if selected_interest_ids and not shared_ids:
            continue

        score = 70  # recipient + occasion + budget are already exact matches
        reasons = ['recipient match', 'occasion match', 'within budget']

        if shared_ids:
            shared_interests = list(gift.interests.filter(id__in=shared_ids))
            score += min(25, 12 + len(shared_ids) * 6)
            reasons.append('interest match')
            interest_phrase = _display_list(shared_interests)
        else:
            interest_phrase = selected_interest_names or 'general gift preferences'

        if marketplace and marketplace != 'any':
            score += 3
            reasons.append(f'{marketplace} match')
        if gift.is_featured:
            score += 2

        why = (
            f"This gift was recommended because it matches the selected recipient, "
            f"fits the chosen occasion, connects with {interest_phrase}, and falls within "
            f"your ₱{budget_min:,.0f}–₱{budget_max:,.0f} budget range."
        )
        results.append({
            'gift': gift,
            'score': min(score, 100),
            'reasons': reasons,
            'why': why,
            'shared_interests': interest_phrase,
        })

    results.sort(key=lambda item: (item['score'], item['gift'].rating, -float(item['gift'].price)), reverse=True)
    return results
