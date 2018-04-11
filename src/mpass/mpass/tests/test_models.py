
# -*- coding: utf-8 -*-


import pytest
from parler.utils.context import switch_language
from mpass.models import AuthenticationSource, AuthenticationTag

@pytest.mark.django_db
def test_create_authsource():
  data = {
    'auth_id': 'testSource',
    'icon_url': 'https://foo.fi/image.png',
    'title': 'test title',
  }
  obj = AuthenticationSource.objects.create(**data)
  for key, val in data.items():
    assert getattr(obj, key) == val


@pytest.mark.django_db
def test_create_authtag():
  data = {
    'tag_id': 'testTag',
    'title': 'test title',
  }
  obj = AuthenticationTag.objects.create(**data)
  for key, val in data.items():
    assert getattr(obj, key) == val


@pytest.mark.django_db
def test_authsource_translation(settings):
  PARLER_LANGUAGES = {
    None: (
        {'code': 'fi',},
        {'code': 'sv',},
    ),
    'default': {
        'fallbacks': ['fi'],
    }
  }
  settings.PARLER_LANGUAGES = PARLER_LANGUAGES
  settings.LANGUAGE_CODE = 'fi'
  data = {
    'auth_id': 'testSource',
    'icon_url': 'https://foo.fi/image.png',
    'title': 'test title',
  }
  obj = AuthenticationSource.objects.create(**data)
  swedish_title = 'titel'
  obj.set_current_language('sv')
  obj.title = swedish_title
  obj.save()

  with switch_language(obj, 'fi'):
    assert obj.title == data['title']
  with switch_language(obj, 'sv'):
    assert obj.title == swedish_title




# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

