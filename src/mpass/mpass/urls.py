
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

from mpass.views import HomeView


urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='mpass_home'),
)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

