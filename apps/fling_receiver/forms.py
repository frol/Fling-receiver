import hashlib
from random import random

from django import forms
from django.utils.crypto import get_random_string

from .models import FlingReceiver


def generate_secret_key():
    while 1:
        secret_key = get_random_string(length=36)
        if not FlingReceiver.objects.filter(secret_key=secret_key).exists():
            break
    return secret_key


class FlingReceiverAddForm(forms.ModelForm):
    
    class Meta:
        model = FlingReceiver
        fields = ('secret_key', )

    def __init__(self, *args, **kwargs):
        initial = kwargs['initial']
        self.user = initial.pop('user')
        if 'secret_key' not in initial:
            initial['secret_key'] = generate_secret_key()
        super(FlingReceiverAddForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        fling_receiver = super(FlingReceiverAddForm, self).save(commit=False)
        fling_receiver.user = self.user
        if commit:
            fling_receiver.save()
        return fling_receiver


class FlingReceiverEditForm(forms.ModelForm):
    
    class Meta:
        model = FlingReceiver
        fields = ('app_id', )

    def __init__(self, *args, **kwargs):
        super(FlingReceiverEditForm, self).__init__(*args, **kwargs)
        # Actually, App ID is 36 chars long, however sometimes after copy-paste it
        # gets space at the begining and then truncate 36th character, which is why
        # I limit max_length to 40 chars instead of 36. Regexp will validate
        # length and format correctly so no worries.
        self.fields['app_id'].widget.attrs['maxlength'] = '40'
        self.fields['app_id'].validators[0].limit_value = 40

    def clean_app_id(self):
        return self.cleaned_data['app_id'].strip()
