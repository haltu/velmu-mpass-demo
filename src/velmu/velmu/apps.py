
# -*- coding: utf-8 -*-

from django.apps import AppConfig


class DefaultConfig(AppConfig):
  name = 'velmu'
  verbose_name = 'velmu'

  def ready(self):
    from mpass.signals import services_updated
    from velmu.signal_handlers import services_updated_handler
    services_updated.connect(services_updated_handler)


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
