from datetime import datetime
import pytz

from django.conf import settings
from django import forms


class CompanyNameForm(forms.Form):
    count = forms.IntegerField(max_value=100, min_value=1, required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    execution_time = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        required=True,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
            'data-target': '#id_execution_time',
            'min': "{:%Y-%m-%dT%H:%M}".format(datetime.now(tz=pytz.timezone(settings.TIME_ZONE)))
        })
    )
