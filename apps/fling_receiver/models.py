from django.conf import settings
from django.core import validators
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


APP_ID_REGEX = r'^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$'

class FlingReceiver(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"))
    app_id = models.CharField(_("App ID"), max_length=36, validators=[
            validators.RegexValidator(APP_ID_REGEX, message=_("Enter a valid App ID."))
        ], help_text=_("App ID has next format: 01234567-890a-bcde-f012-0123456789ab"))
    secret_key = models.CharField(_("Secret key"), max_length=36, unique=True)

    def get_secret_absolute_url(self):
        return 'http://%s%s' % (settings.SITE_DOMAIN,
            reverse('fling_receiver_template', args=(self.secret_key, )))
