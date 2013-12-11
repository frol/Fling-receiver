from django.conf.urls import patterns, url
from django.contrib.auth.views import password_reset, password_reset_done, \
    password_reset_confirm, password_reset_complete, password_reset_confirm_uidb36

from .forms import PasswordResetForm


urlpatterns = patterns('auth_ext.views',
    # Sign up, Login and Logout
    url(r'^signup/$', 'signup', {'success_url': 'fling_receiver_add'}, name="auth_signup"),
    url(r'^login/$', 'login', name="auth_login"),
    # Email confirmation
    url(r'^confirmation/send/$', 'send_confirm_email', name='auth_email_confirmation'),
    url(r'^confirm_email/(\w+)/$', 'confirm_email', name="auth_confirm_email"),
)

# Password reset (django.contib.auth urls redefinition)
urlpatterns += patterns('django.contrib.auth.views',
    url(r'^logout/$', 'logout', {'next_page': '/'}, name="auth_logout"),
    url(r'^logout/(?P<next_page>.*)/$', 'logout', name="auth_logout_next"),
)

urlpatterns += patterns('misc.views',
    url(r'^language/(?P<lang>\w+)/$', 'language_change', name="auth_language_change"),
)

# Password reset (django.contib.auth urls redefinition with Jinja2 rendering)
urlpatterns += patterns('misc.views',
    url(r'^password_reset/$', 'coffin_template_response', {
            'template_name': 'auth/password_reset_form.html',
            'view': password_reset,
            'password_reset_form': PasswordResetForm,
            'subject_template_name': 'auth/password_reset_subject.txt',
            'post_reset_redirect': 'auth_password_reset_done',
            'email_template_name': 'auth/password_reset_email.html'
         }, name="auth_password_reset"),
    url(r'^password_reset_done/$', 'coffin_template_response', {
            'template_name': 'auth/password_reset_done.html',
            'view': password_reset_done
         }, name="auth_password_reset_done"),
    url(r'^password_reset_confirm/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'coffin_template_response', {
            'template_name': 'auth/password_reset_confirm.html',
            'view': password_reset_confirm_uidb36,
        }, name='auth_password_reset_confirm_uidb36'),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'coffin_template_response', {
            'template_name': 'auth/password_reset_confirm.html',
            'view': password_reset_confirm,
            'post_reset_redirect': 'auth_password_reset_complete',
        }, name='auth_password_reset_confirm'),
    url(r'^password_reset_complete/$', 'coffin_template_response', {
            'template_name': 'auth/password_reset_complete.html',
            'view': password_reset_complete
         }, name="auth_password_reset_complete"),
)
