# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# All rights reserved.
#

import logging
from celery import task
from django.utils import timezone, translation
from mpass import settings
from mpass.api import MPASSAPI, MPASSError
from mpass.models import AuthenticationSource, AuthenticationTag, Service
from mpass.signals import services_updated

LOG = logging.getLogger(__name__)


@task(ignore_result=True)
def fetch_mpass_authentication_sources():
  fetch_mpass_authentication_tags()
  api_client = MPASSAPI()
  start_time = timezone.now()
  for lang in settings.LANGUAGES:
    with translation.override(lang):
      try:
        auth_sources = api_client.get_authentication_sources(lang=lang)
      except MPASSError:
        LOG.error('MPASS authentication sources fetch failed', exc_info=True,
                  extra={'data': {'language': lang}})
        continue
      for auth_source in auth_sources:
        attributes = {
          'icon_url': auth_source.get('iconUrl'),
          'title': auth_source.get('title'),
        }
        auth_source_obj, created = AuthenticationSource.objects.get_or_create(
          auth_id=auth_source['id'], defaults=attributes.copy()
        )
        if not created:
          for key, value in attributes.items():
            setattr(auth_source_obj, key, value)
          auth_source_obj.save()
        auth_source_obj.tags.add(
          *AuthenticationTag.objects.filter(tag_id__in=auth_source['tags'])
        )
  AuthenticationSource.objects.filter(modified_at__lt=start_time).delete()


@task(ignore_result=True)
def fetch_mpass_authentication_tags():
  api_client = MPASSAPI()
  start_time = timezone.now()
  for lang in settings.LANGUAGES:
    with translation.override(lang):
      try:
        auth_tags = api_client.get_authentication_tags(lang=lang)
      except MPASSError:
        LOG.error('MPASS authentication tags fetch failed', exc_info=True,
                  extra={'data': {'language': lang}})
        continue
      for auth_tag in auth_tags:
        attributes = {
          'title': auth_tag.get('title'),
        }
        auth_tag_obj, created = AuthenticationTag.objects.get_or_create(
          tag_id=auth_tag['id'], defaults=attributes.copy()
        )
        if not created:
          for key, value in attributes.items():
            setattr(auth_tag_obj, key, value)
          auth_tag_obj.save()
  AuthenticationTag.objects.filter(modified_at__lt=start_time).delete()


@task(ignore_result=True)
def fetch_mpass_services():
  api_client = MPASSAPI()
  start_time = timezone.now()
  # services endpoint does not currently support language selection
  lang = 'fi'
  api_lang = None
  service_objects = []
  with translation.override(lang):
    try:
      services = api_client.get_services(lang=api_lang)
    except MPASSError:
      LOG.error('MPASS services fetch failed', exc_info=True,
                extra={'data': {'language': lang}})
      return
    for service in services:
      attributes = {
        'icon_url': service.get('iconUrl'),
        'title': service.get('title'),
        'description': service.get('description'),
        'service_url': service.get('serviceUrl'),
        'sso_url': service.get('ssoUrl'),
      }
      service_obj, created = Service.objects.get_or_create(
        service_id=service['id'], defaults=attributes.copy()
      )
      if not created:
        for key, value in attributes.items():
          setattr(service_obj, key, value)
        service_obj.save()

  Service.objects.filter(modified_at__lt=start_time).delete()
  services_updated.send(sender=Service)


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

