from django import forms
from .choices import MARKETPLACE_CHOICES, OCCASION_CHOICES, RECIPIENT_CHOICES
from .models import Interest


BUDGET_CHOICES = [
    ('0-500', '₱0 - ₱500'),
    ('500-1500', '₱500 - ₱1,500'),
    ('1500-5000', '₱1,500 - ₱5,000'),
    ('5000-999999', '₱5,000+'),
]


class GiftFinderForm(forms.Form):
    recipient_type = forms.ChoiceField(choices=RECIPIENT_CHOICES, widget=forms.RadioSelect)
    occasion_type = forms.ChoiceField(choices=OCCASION_CHOICES)
    recipient_name = forms.CharField(required=False, widget=forms.HiddenInput)
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    budget_range = forms.ChoiceField(choices=BUDGET_CHOICES)
    marketplace = forms.ChoiceField(choices=MARKETPLACE_CHOICES, required=False, initial='any')

    def budget_min_max(self):
        value = self.cleaned_data.get('budget_range', '0-999999')
        low, high = value.split('-')
        return int(low), int(high)
