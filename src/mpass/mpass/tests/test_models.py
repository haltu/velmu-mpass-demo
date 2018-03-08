
# -*- coding: utf-8 -*-

"""
Tests for the models of the ``mpass`` app.

"""
from django.test import TestCase

from mpass.tests.factories import ExampleFactory


class ExampleTestCase(TestCase):
  """Tests for the ``Example`` model class."""
  def test_model(self):
    obj = ExampleFactory()
    self.assertTrue(obj.pk)


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

