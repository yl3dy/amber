# -*- coding: utf-8 -*-
'''Pages url patterns'''
from django.conf.urls.defaults import patterns, url
from amber.views import mainpage, servers_page

# pylint: disable-msg=C0103
urlpatterns = patterns('',
    url(r'^$', mainpage),
    url(r'^servers/$', servers_page),
    (r'^about/$', 'django.views.generic.simple.direct_to_template', \
        {'template': 'about.html'}),
    (r'^settings/$', 'django.views.generic.simple.direct_to_template', \
        {'template': 'settings.html'}),
)
