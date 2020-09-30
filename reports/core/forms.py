from django.forms import ModelForm
from django.forms import HiddenInput
from .models import Entity
from django.core.exceptions import ValidationError


class CreateEntityForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateEntityForm, self).__init__(*args, **kwargs)

    def clean_duration(self):
        # automatically raised method when cleaning field 'term'
        # during form validation . return data is MUST
        data = self.cleaned_data['duration']
        if data < 5:
            raise ValidationError('Too short duration, is it possible, bro?', code='invalid')
        return data

    class Meta:
        model = Entity
        fields = ['user_id', 'date', 'duration', 'distance']

        widgets = {
            'user_id': HiddenInput,
                   }
