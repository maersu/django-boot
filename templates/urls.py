from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin_tools/', include('admin_tools.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    # Using this method is inefficient and insecure. Do not use this in a production setting. Use this only for development.
    urlpatterns += patterns('', (r'^admin_tools/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '../../../{{projectname}}-env/lib/python2.6/site-packages/admin_tools/media/admin_tools/', 'show_indexes': True}), )
    urlpatterns += patterns('', (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}), )

