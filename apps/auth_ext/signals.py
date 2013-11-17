from django.conf import settings
from django.dispatch import Signal, receiver
from django.utils.translation import ugettext, activate


email_confirmed = Signal(providing_args=["user"])
signup_done = Signal(providing_args=["user"])


if 'misc' in settings.INSTALLED_APPS:
    from misc.signals import language_changed

    @receiver(language_changed)
    def language_changed_callback(sender, **kwargs):
        activate(kwargs['lang'])
        kwargs['request'].user.message_set.create(message=ugettext(u"Language successfully updated."))
