
# -*- coding: utf-8 -*-

from django.conf import settings

APP_URL = getattr(settings, 'VELMU_APP_URL', 'localhost')
# PERSISTENT_ACCOUNTS are whitelisted MPASS accounts which get to keep their desktops
PERSISTENT_ACCOUNTS = getattr(settings, 'VELMU_PERSISTENT_ACCOUNTS', [])

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

