import re

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.translation import ugettext_lazy as _, ugettext

from .models import EmailConfirmation

User = get_user_model()
alnum_re = re.compile(r'^[\w\-_.]+$')


class LoginForm(forms.Form):
    
    username = forms.CharField(label=_("Email"), max_length=30, widget=forms.TextInput())
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(render_value=False))
    remember = forms.BooleanField(label=_("Remember Me"), help_text=_("If checked you will stay logged in for 2 weeks"), required=False, initial=True)
    
    def clean(self):
        if self._errors:
            return
        user = authenticate(username=self.cleaned_data["username"], password=self.cleaned_data["password"])
        if user:
            if user.is_active:
                self.user = user
            else:
                raise forms.ValidationError(_("This account is currently inactive."))
        else:
            raise forms.ValidationError(_("The username and/or password you specified are not correct."))
        return self.cleaned_data
    

class SignupForm(forms.Form):
    
    email = forms.EmailField(label = _("Email"), required = True, widget = forms.TextInput())
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=_("Password (again)"),
        widget=forms.PasswordInput(render_value=False))
    
    def clean(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(_("User with this email already exists."))
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data
    
    def save(self):
        username = email = self.cleaned_data["email"]
        password = self.cleaned_data["password1"]
        new_user = User.objects.create_user(username, email, password)
        #EmailConfirmation.objects.send_confirmation(new_user)
        #new_user.message_set.create(message=ugettext(u"Confirmation email sent to %(email)s") % {'email': email})
        if settings.ACCOUNT_EMAIL_VERIFICATION:
            new_user.is_active = False
            new_user.save()
        return username, password # required for authenticate()
