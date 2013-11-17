# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from random import random, randint
import os
import sys
import urllib

from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin, \
    AnonymousUser, SiteProfileNotAvailable
from django.db import models
from django.db.models.base import ModelBase
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, ugettext

from .managers import EmailConfirmationManager


class EmailConfirmation(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    sent = models.DateTimeField()
    confirmation_key = models.CharField(max_length=40)

    objects = EmailConfirmationManager()

    def key_expired(self):
        expiration_date = self.sent + timedelta(
            days=settings.EMAIL_CONFIRMATION_DAYS)
        return expiration_date <= datetime.now()

    def __unicode__(self):
        return ugettext("Confirmation for %(user)s, email - %(email)s" % {'user': self.user, 'email': self.user.email})

    class Meta:
        verbose_name = _("E-mail confirmation")
        verbose_name_plural = _("E-mail confirmations")


URL_LOGIN_TOKEN_LENGTH = 20
        
class UrlLoginToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    token = models.CharField(_("Token"), max_length=URL_LOGIN_TOKEN_LENGTH)
    expires = models.DateTimeField(_("Expires"))

    @classmethod
    def get_object(cls, **kwargs):
        try:
            obj = cls.objects.get(**kwargs)
            if obj.expires < datetime.now():
                obj.delete()
            else:   
                return obj
        except cls.DoesNotExist:
            pass
        return None

    @classmethod
    def get_token(cls, user):
        obj = cls.get_object(user=user)
        if obj:
            obj.expires = datetime.now() + timedelta(days=settings.URL_LOGIN_EXPIRES_DAYS)
        else:
            token = '%.5x' % randint(0, 16**URL_LOGIN_TOKEN_LENGTH)
            obj = cls(user=user, token=token, expires=datetime.now() + timedelta(days=settings.URL_LOGIN_EXPIRES_DAYS))
        obj.save()
        return obj.token


class User(AbstractBaseUser, PermissionsMixin):
    username = models.EmailField(_("Username"), unique=True)
    first_name = models.CharField(_("First name"), max_length=30, blank=True)
    last_name = models.CharField(_("Last name"), max_length=30, blank=True)
    email = models.EmailField(_("Email address"), blank=True, unique=True)
    is_staff = models.BooleanField(_("Staff status"), default=False,
        help_text=_("Designates whether the user can log into this admin "
                    "site."))
    is_active = models.BooleanField(_("Active"), default=True,
        help_text=_("Designates whether this user should be treated as "
                    "active. Unselect this instead of deleting accounts."))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    # Additional information to User
    language = models.CharField(_("Language"), max_length=10, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)
    email_verified = models.BooleanField(_("Email confirmed"), default=not settings.ACCOUNT_EMAIL_VERIFICATION)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def get_profile(self):
        raise SiteProfileNotAvailable

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = self.username
        return super(User, self).save(*args, **kwargs)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])
