from django import forms
from django.utils.translation import ugettext as _

from tours.models import UserFeedback


class UserForm(forms.ModelForm):
    class Meta:
        model = UserFeedback
        fields = ['origin', 'background', 'method', 'feedback']
        labels = {
            'origin': 'Where are you from?',
            'background': 'Who are you?',
            'method': 'How did you take the tour?',
            'feedback': 'Want to leave feedback? Do it here!'
        }
        widgets = {
            'origin': forms.Select(attrs={"class": "form-control"}),
            'background': forms.Select(attrs={"class": "form-control"}),
            'method': forms.Select(attrs={"class": "form-control"}),
            'feedback': forms.Textarea(attrs={'rows': 5, "class": "form-control"})
        }
