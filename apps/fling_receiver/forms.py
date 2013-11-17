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


