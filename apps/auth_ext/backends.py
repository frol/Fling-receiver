from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import check_password
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import UrlLoginToken

User = get_user_model()

class UserNameAndEmailAuthBackend(ModelBackend):

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(Q(email=username)|Q(username=username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass
        return None


class UrlTokenBackend(object):

    supports_anonymous_user = False
    supports_inactive_user = False
    supports_object_permissions = False

    def authenticate(self, token=None):
        url_login_token = UrlLoginToken.get_object(token=token)
        if url_login_token:
            return url_login_token.user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

