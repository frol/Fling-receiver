# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse

LOGIN_REDIRECT_URLNAME = getattr(settings, "LOGIN_REDIRECT_URLNAME", '')

def get_default_redirect(request, redirect_field_name="next",
        login_redirect_urlname=LOGIN_REDIRECT_URLNAME):
    """
    Returns the URL to be used in login procedures by looking at different
    values in the following order:
    
    - LOGIN_REDIRECT_URLNAME - the name of a URLconf entry in the settings
    - LOGIN_REDIRECT_URL - the URL in the setting
    - a REQUEST value, GET or POST, named "next" by default.
    """
    redirect_to = request.REQUEST.get(redirect_field_name)
    # light security check -- make sure redirect_to isn't garbage.
    if not redirect_to or "://" in redirect_to or " " in redirect_to:
        redirect_to = login_redirect_urlname
    return redirect_to
