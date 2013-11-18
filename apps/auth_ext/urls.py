from django.conf.urls import patterns, url
from django.contrib.auth.views import password_reset, password_reset_done, \
    password_reset_confirm, password_reset_complete

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
    # Reset password
    url(r'^password_reset/$', 'coffin_template_response', {
        'view': password_reset,
        'template_name': 'auth/password_reset_form.html',
        'email_template_name': 'auth/password_reset_email.html'}, name="auth_password_reset"),
    url(r'^password_reset_done/$', 'coffin_template_response', {
        'view': password_reset_done, 
        'template_name': 'auth/password_reset_done.html'}, name="auth_password_reset_done"),
    url(r'^password_reset_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'coffin_template_response', {
        'view': password_reset_confirm,
        'template_name': 'auth/password_reset_confirm.html'}, name="auth_password_reset_confirm"),
    url(r'^password_reset_complete/$', 'coffin_template_response', {
        'view': password_reset_complete,
        'template_name': 'auth/password_reset_complete.html'}, name="auth_password_reset_complete"),
)
