
# -*- coding: utf-8 -*-

import pytest
from mpass.models import AuthenticationSource, AuthenticationTag


@pytest.fixture()
def auth_tag():
  return AuthenticationTag.objects.create(tag_id='testTag1', title='tag title1')


@pytest.fixture()
def auth_source(auth_tag):
  source = AuthenticationSource.objects.create(auth_id='testSource1',
                                               title='source title1',
                                               icon_url='http://localhost/foo.jpg')
  source.tags.add(auth_tag)
  return source



# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

