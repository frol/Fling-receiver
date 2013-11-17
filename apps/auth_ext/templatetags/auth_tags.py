from django.conf import settings

if 'coffin' in settings.INSTALLED_APPS:
    from coffin.template import Library
else:
    from django.template import Library

from auth_ext.forms import LoginForm, SignupForm


register = Library()

if 'coffin' in settings.INSTALLED_APPS:
    register.simple_tag = register.object

@register.simple_tag
def get_signup_form():
    return SignupForm()

@register.simple_tag
def get_login_form():
    return LoginForm()
