
# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# All rights reserved.
#

from django.conf import settings


IDP_URL = getattr(settings, 'MPASS_IDP_URL', 'https://mpass-proxy.csc.fi')
REQUESTS_TIMEOUT = getattr(settings, 'MPASS_REQUESTS_TIMEOUT', 3)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

