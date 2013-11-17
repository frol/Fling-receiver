from django.conf.urls import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('fling_receiver.urls')),
    (r'^auth/', include('auth_ext.urls')),

    (r'^admin/', include(admin.site.urls)),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
