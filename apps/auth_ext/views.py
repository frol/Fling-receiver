# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login as auth_login
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _, ugettext

if 'coffin' in settings.INSTALLED_APPS:
    from coffin.template.response import TemplateResponse
else:
    from django.template.response import TemplateResponse

from .forms import LoginForm, SignupForm
from .models import EmailConfirmation
from .signals import signup_done
from .utils import get_default_redirect

User = get_user_model()
logger = logging.getLogger(__name__)

import os
from misc.json_encode import json_response, JSONTemplateResponse

def ajax(func):
    def wrapped_func(request, *args, **kwargs):
        func_response = func(request, *args, **kwargs)
        if not request.is_ajax():
            return func_response
        if isinstance(func_response, HttpResponseRedirect):
            return json_response({'status': 'ok', 'action': 'redirect',
                'url': func_response._headers['location'][1]})
        if isinstance(func_response, TemplateResponse):
            template_name_splitted = os.path.splitext(func_response.template_name)
            template_name = template_name_splitted[0] + '_ajax' + template_name_splitted[1]
            return JSONTemplateResponse(request, template_name,
                func_response.context_data, data={'status': 'ok'})
        return func_response
    return wrapped_func


@ajax
def login(request, form_class=LoginForm, template_name='auth/login.html', success_url=None):
    if success_url is None:
        success_url = get_default_redirect(request)
    form = form_class(request.POST or None)
    if form.is_valid():
        auth_login(request, form.user)
        request.user_remember = form.cleaned_data['remember']
        return redirect(success_url)
    return TemplateResponse(request, template_name, {'form': form})

def post_signup(request, username, password):
    new_user = get_object_or_404(User, username=username)
    signup_done.send(sender=User, user=new_user)
    if new_user.is_active:
        user = authenticate(username=username, password=password)
        auth_login(request, user)

@ajax
def signup(request, form_class=SignupForm, template_name='auth/signup.html', success_url=None):
    if success_url is None:
        success_url = get_default_redirect(request)
    form = form_class(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username, password = form.save()
        post_signup(request, username, password)
        return redirect(success_url)
    return TemplateResponse(request, template_name, {'form': form})

def send_confirm_email(request):
    EmailConfirmation.objects.send_confirmation(request.user)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def confirm_email(request, confirmation_key, template_name='emailconfirmation/confirm_email.html'):
    confirmation_key = confirmation_key.lower()
    email_address = EmailConfirmation.objects.confirm_email(confirmation_key)
    return TemplateResponse(request, template_name, {'email_address': email_address})
