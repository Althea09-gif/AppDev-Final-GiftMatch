from django import forms
from .models import Occasion


class OccasionForm(forms.ModelForm):
    class Meta:
        model = Occasion
        fields = ['event_title', 'recipient_name', 'occasion_type', 'event_date', 'reminder_days_before', 'notes']
        widgets = {
            'event_title': forms.TextInput(attrs={
                'placeholder': "Examples: Mom's Birthday, Wedding Anniversary, Graduation Day, Christmas Celebration"
            }),
            'recipient_name': forms.TextInput(attrs={
                'placeholder': 'Examples: Maria Santos, John Cruz, Mom, Best Friend'
            }),
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional notes, delivery reminders, or gift ideas'}),
        }
