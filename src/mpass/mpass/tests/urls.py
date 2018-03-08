
# -*- coding: utf-8 -*-

"""
This ``urls.py`` is only used when running the tests via ``runtests.py``.
"""
from django.conf.urls.defaults import include, patterns, url


urlpatterns = patterns('',
    url(r'^', include('mpass.urls')),
)


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

