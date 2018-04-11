# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# All rights reserved.
#

import logging
import requests
from mpass import settings


LOG = logging.getLogger(__name__)


class MPASSError(Exception):
  pass


class MPASSAPI(object):
  def __init__(self, idp_url=settings.IDP_URL, *args, **kwargs):
    self.idp_url = idp_url.rstrip('/')
    super(MPASSAPI, self).__init__(*args, **kwargs)

  def get_authentication_sources(self, lang=None):
    endpoint = '/idp/profile/api/authnsources'
    if lang is not None:
      return self._get_request(endpoint, {'lang': lang})
    else:
      return self._get_request(endpoint)

  def get_authentication_tags(self, lang=None):
    endpoint = '/idp/profile/api/authntags'
    if lang is not None:
      return self._get_request(endpoint, {'lang': lang})
    else:
      return self._get_request(endpoint)

  def get_services(self, lang=None):
    endpoint = '/idp/profile/api/services'
    if lang is not None:
      return self._get_request(endpoint, {'lang': lang})
    else:
      return self._get_request(endpoint)

  def _get_request(self, endpoint, params=None):
    if params is None:
      params = {}
    headers = {'Accept': 'application/json'}
    try:
      response = requests.get(self.idp_url + endpoint, params=params,
                              headers=headers, timeout=settings.REQUESTS_TIMEOUT)
      response.raise_for_status()
      return response.json()['response']
    except requests.RequestException as e:
      LOG.exception('MPASS API call failed')
      raise MPASSError(e)
    except ValueError as e:
      LOG.error('MPASS response was not JSON', exc_info=True, extra={'data': {
        'response_content': response.content,
        'response_status': response.status_code
      }})
      raise MPASSError(e)
    except KeyError as e:
      LOG.error('MPASS response did not contain response', exc_info=True, extra={
        'data': {
          'response_content': response.content,
          'response_status': response.status_code
        }})
      raise MPASSError(e)



# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

