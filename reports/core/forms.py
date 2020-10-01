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

    def is_valid(self):
        return super().is_valid() and self.valid_speed()

    def valid_speed(self):
        dst = self.cleaned_data['distance']
        dr = self.cleaned_data['duration']
        if dr == 0:
            self.errors['duration'] = 'Duration can\'t be zero'
            return False
        av_speed = dst / dr
        if av_speed > 250:
            self.errors['Average Speed'] = ' is too high!'
            return False
        if av_speed < 5:
            self.errors['Average Speed'] = ' is too low!'
            return False
        return True

    class Meta:
        model = Entity
        fields = ['user_id', 'date', 'duration', 'distance']

        widgets = {
            'user_id': HiddenInput,
                   }
