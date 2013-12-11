import re

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.encoding import force_bytes

try:
    from coffin.template.loader import render_to_string
except ImportError:
    from django.template.loader import render_to_string

from .models import EmailConfirmation

send_html_mail = None

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


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def save(self, domain_override=None,
             subject_template_name='auth/password_reset_subject.txt',
             email_template_name='auth/password_reset_email.html',
             email_template_name_txt='auth/password_reset_email.txt',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        users = UserModel._default_manager.filter(email__iexact=email)
        for user in users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable
            if not user.has_usable_password():
                continue
            from django.template import RequestContext
            request_context = RequestContext(request)
            c = {
                'email': user.email,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                'SITE_DOMAIN': settings.SITE_DOMAIN,
            }
            subject = render_to_string(subject_template_name, c, context_instance=request_context)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            body_txt = render_to_string(email_template_name_txt, c, context_instance=request_context)
            if send_html_mail:
                body_html = render_to_string(email_template_name, c, context_instance=request_context)
                send_html_mail(subject, body_txt, body_html, from_email, [user.email])
            else:
                send_mail(subject, body_txt, from_email, [user.email])
