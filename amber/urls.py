from django.conf.urls.defaults import patterns, include, url
from views import mainpage

urlpatterns = patterns('',
    url(r'^$', mainpage),
)
