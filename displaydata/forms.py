from django import forms

from enterdata.models import Category
from . import models
from django.utils.datastructures import MultiValueDictKeyError


class DateInput(forms.DateInput):
    input_type = 'date'

class DisplayData(forms.ModelForm):
    from_date = forms.DateField(widget= DateInput)
    to_date = forms.DateField(widget= DateInput)
    
    class Meta:
        model = models.DisplayForm
        fields = ['species_name', 'in_country', 'in_county', 'from_date', 'to_date']

    def __init__(self, *args, **kwargs):
        try:
            self.name = args[0]['name']
            # print(self.name)
            category = Category.objects.get(name = self.name)
            super(DisplayData, self).__init__(*args, **kwargs)
            self.fields['species_name'].queryset = models.Species.objects.filter(category = category)
            # print('self.fields')
            # print(self.fields)

        except MultiValueDictKeyError:
            super(DisplayData, self).__init__(*args, **kwargs)