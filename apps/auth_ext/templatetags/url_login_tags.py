from django.conf import settings

if 'coffin' in settings.INSTALLED_APPS:
    from coffin.template import Library
else:
    from django.template import Library

from auth_ext_15.models import UrlLoginToken

register = Library()

@register.simple_tag
def url_login_token(user):
    return "url_login_token=%s" % UrlLoginToken.get_token(user)
