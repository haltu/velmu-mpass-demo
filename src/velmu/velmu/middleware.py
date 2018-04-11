
# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# All rights reserved.
#


METHOD_OVERRIDE_HEADER = 'HTTP_X_HTTP_METHOD_OVERRIDE'


class MethodOverrideMiddleware(object):
  """
  DRF 3.30 no longer supports the X-HTTP-Method-Override header we are
  using in XMLHttpRequests. This Middleware emulates the support.
  """
  def process_view(self, request, callback, callback_args, callback_kwargs):
    if request.method != 'POST':
      return
    if METHOD_OVERRIDE_HEADER not in request.META:
      return
    request.method = request.META[METHOD_OVERRIDE_HEADER]

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2


