from django.conf.urls import patterns, url

urlpatterns = patterns('fling_receiver.views',
    url('^$', 'root', name='root'),
    url('^fling_receiver/$', 'fling_receiver_list', name='fling_receiver_list'),
    url('^fling_receiver/add/$', 'fling_receiver_add', name='fling_receiver_add'),
    url('^fling_receiver/edit/(?P<fling_receiver_id>\d+)/$', 'fling_receiver_edit', name='fling_receiver_edit'),
    url('^fling_receiver/predelete/(?P<fling_receiver_id>\d+)/$', 'fling_receiver_predelete', name='fling_receiver_predelete'),
    url('^fling_receiver/delete/$', 'fling_receiver_delete', name='fling_receiver_delete'),
    url('^freceiver/(?P<secret_key>\w+)/index.html$', 'fling_receiver_template', name='fling_receiver_template'),
)
