
# -*- coding: utf-8 -*-

import logging
import requests
from io import BytesIO
from django.core.files.images import ImageFile
from django.utils.timezone import now
from django.utils.translation import activate
from dreamcards.models import Card, Category
from mpass.models import Service

LOG = logging.getLogger(__name__)
MPASS_CARD_CATEGORY = 'MPASS'


def services_updated_handler(**kwargs):
  """
  Update system cards in the MPASS category based on Services fetched from MPASS
  API
  """
  activate('fi')
  services = Service.objects.active_translations('fi')
  card_qs = Card.objects.filter(
    category__title=MPASS_CARD_CATEGORY, owner__isnull=True
  )
  start_time = now()
  for service in services:
    try:
      _update_mpass_service_card(card_qs.get(url=service.sso_url), service)
    except Card.DoesNotExist:
      _create_mpass_service_card(service)
  # deactivate cards in MPASS category if there no longer was a service for it
  for card in card_qs.filter(modified__lt=start_time):
    card.active = False
    card.save()


def _update_mpass_service_card(instance, service):
  # TODO: update icon of existing card. no way to see whether the icon has changed.
  # perhaps implement a new card type having icon as url or just do that in
  # the base Card model.
  for key, value in _get_card_attributes_from(service).items():
    setattr(instance, key, value)
  instance.active = True
  instance.save()
  if instance.thumbnail is None:
    _fetch_and_save_card_icon(instance, service)
  return instance


def _create_mpass_service_card(service):
  category, _cat_created = Category.objects.get_or_create(
    title=MPASS_CARD_CATEGORY
  )
  instance = Card.objects.create(
    category=category, **_get_card_attributes_from(service)
  )
  _fetch_and_save_card_icon(instance, service)
  return instance


def _get_card_attributes_from(service):
  return {
    'title': service.title,
    'url': service.sso_url,
  }


def _fetch_and_save_card_icon(card, service):
  icon_filename = _get_icon_filename_from(service)
  if icon_filename:
    card.thumbnail.save(icon_filename, _fetch_icon_from(service), save=True)


def _get_icon_filename_from(service):
  if not service.icon_url:
    return None
  _base, slash, name = service.icon_url.rpartition('/')
  if slash:
    return name
  return None


def _fetch_icon_from(service):
  if not service.icon_url:
    return None
  try:
    response = requests.get(service.icon_url, timeout=3)
    return ImageFile(BytesIO(response.content))
  except:
    LOG.error('MPASS Service icon fetch failed', exc_info=True, extra={
      'data': {'service_id': service.service_id, 'icon_url': service.icon_url}
    })
    return None


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

