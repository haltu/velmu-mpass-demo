
# -*- coding: utf-8 -*-

from django.conf.urls import url
from mpass.views import MPASSLoginView


urlpatterns = [
  url(r'^$', MPASSLoginView.as_view(), name='mpass.login'),
]

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

