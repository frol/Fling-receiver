from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import EmailConfirmation, UrlLoginToken

User = get_user_model()

admin.site.register(EmailConfirmation)
admin.site.register(User, UserAdmin)
admin.site.register(UrlLoginToken)
