from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns(
    'microdash.core.views',
    url(r'^$', 'station_dashboard', name='home'),
    url(r'^(?P<shortcode>[-\w]+)/$', 'station_dashboard', name='station'),
)
