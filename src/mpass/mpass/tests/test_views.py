
# -*- coding: utf-8 -*-

import pytest
from django.contrib.auth.models import AnonymousUser
from mpass import views


@pytest.mark.django_db
def test_get_loginview(auth_source, rf):
  request = rf.get('/login')
  request.user = AnonymousUser()
  response = views.MPASSLoginView.as_view()(request)
  assert response.status_code == 200
  response.render()


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

