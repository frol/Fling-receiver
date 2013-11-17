# -*- coding: utf-8 -*-
import re

from django.contrib.auth import authenticate, login
from django.contrib.auth.middleware import AuthenticationMiddleware as BaseAuthenticationMiddleware
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed


class AuthenticationMiddleware(BaseAuthenticationMiddleware):

    def process_request(self, request):
        res = super(AuthenticationMiddleware, self).process_request(request)
        self.authenticated = request.user.is_authenticated()
        request.user_remember = True
        if 'url_login_token' in request.GET:
            user = authenticate(token=request.GET['url_login_token'])
            if user:
                login(request, user)
        return res

    def process_response(self, request, response):
        if not hasattr(request, 'session'):
            return response
        if not self.authenticated and request.user.is_authenticated():
            if request.user_remember:
                max_age = settings.SESSION_COOKIE_AGE
                request.session.set_expiry(max_age)
                response.set_cookie('logined', request.user.username, max_age=max_age)
            else:
                request.session.set_expiry(0)
                response.set_cookie('logined', request.user.username)
        elif self.authenticated and not request.user.is_authenticated():
            response.delete_cookie('logined')
        return response
