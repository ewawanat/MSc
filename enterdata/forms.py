from django import forms
from django.forms.widgets import DateInput
from . import models
import datetime
from django.core.validators import MaxValueValidator
from django.utils.datastructures import MultiValueDictKeyError


class DateInput(forms.DateInput):
    input_type = 'date'

class EnterData(forms.ModelForm):
    date_seen = forms.DateField(widget = DateInput, validators = [MaxValueValidator(datetime.date.today)])

    class Meta:
        model = models.Sighting
        fields = ['species', 'date_seen', 'photo', 'in_country', 'in_county' ]

    def __init__(self, *args, **kwargs):
        try:
            self.name = args[0]['name']
            # print(self.name)
            super(EnterData, self).__init__(*args, **kwargs)
            self.fields['species'].queryset = models.Species.objects.filter(category = self.name)
        except MultiValueDictKeyError:
            super(EnterData, self).__init__(*args, **kwargs)
