import re

from django import forms
from django.core.exceptions import ValidationError


class CityForm(forms.Form):
    city_name = forms.CharField(
        label='Get weather',
        max_length=100,
        widget =forms.TextInput(attrs={
            'placeholder': 'Input city name...',
        }),
    )

