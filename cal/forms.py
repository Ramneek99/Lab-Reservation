from django.forms import ModelForm, DateInput, forms, DateField
from cal.models import Event
import datetime
from django.forms import SelectDateWidget


class EventForm(ModelForm):
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        # start_time = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'],widget=forms.DateTimeInput( attrs={'type': 'datetime-local','class': 'form-control'},format='%Y-%m-%dT%H:%M'))
        # end_time = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'],widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'},format='%Y-%m-%dT%H:%M'))
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        # widgets ={
        #     'date_for_lab': DateInput(attrs={'class':'datepicker'}, format='%Y/%m/%d'),
        #     'start_time': DateInput(attrs={'class':'timepicker'}, format='%H:%i:%A'),
        #     'end_time': DateInput(attrs={'class': 'timepicker'}, format='%H:%i:%A')
        # }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
