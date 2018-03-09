# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# All rights reserved.
#

from django.contrib import admin
from parler.admin import TranslatableAdmin
from mpass import models


class AuthenticationSourceAdmin(TranslatableAdmin):
  search_fields = ('translations__title', 'auth_id')
  list_display = ('title', 'auth_id')
  date_hierarchy = 'created_at'
  ordering = ('auth_id',)


class AuthenticationTagAdmin(TranslatableAdmin):
  search_fields = ('translations__title', 'tag_id')
  list_display = ('title', 'tag_id')
  date_hierarchy = 'created_at'
  ordering = ('tag_id',)


admin.site.register(models.AuthenticationSource, AuthenticationSourceAdmin)
admin.site.register(models.AuthenticationTag, AuthenticationTagAdmin)


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

