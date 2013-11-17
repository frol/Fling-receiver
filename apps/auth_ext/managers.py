from datetime import datetime
from hashlib import sha1 as sha
from random import random

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string

if 'mailer' in settings.INSTALLED_APPS:
    from mailer import send_mail
else:
    from django.core.mail import send_mail

from .signals import email_confirmed


class EmailConfirmationManager(models.Manager):

    def confirm_email(self, confirmation_key):
        try:
            confirmation = self.get(confirmation_key=confirmation_key)
        except self.model.DoesNotExist:
            return False
        if not confirmation.key_expired():
            user = confirmation.user
            user.is_active = True
            user.email_verified = True
            user.save()
            email_confirmed.send(sender=self.model, user=user)
            return True
        return False

    def send_confirmation(self, user):
        salt = sha(str(random())).hexdigest()[:5]
        confirmation_key = sha(salt + user.email).hexdigest()
        path = reverse("auth_confirm_email", args=[confirmation_key])
        protocol = getattr(settings, 'MY_SITE_PROTOCOL', 'http')
        port     = getattr(settings, 'MY_SITE_PORT', '')
        activate_url = u"%s://%s%s%s" % (protocol, settings.SITE_DOMAIN, port and ':' + port or '', path)
        context = {
            "user": user,
            "activate_url": activate_url,
            "site_name": settings.SITE_NAME,
            "confirmation_key": confirmation_key,
        }
        subject = render_to_string("auth/email_confirmation_subject.txt", context)
        subject = "".join(subject.splitlines()) # remove superfluous line breaks
        message = render_to_string("auth/email_confirmation_message.txt", context)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return self.create(user=user, sent=datetime.now(), confirmation_key=confirmation_key)

    def delete_expired_confirmations(self):
        for confirmation in self.all():
            if confirmation.key_expired():
                confirmation.delete()
