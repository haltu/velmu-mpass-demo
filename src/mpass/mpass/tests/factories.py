
# -*- coding: utf-8 -*-

"""
Factories for the ``mpass`` app.

Always provide factories for all your models. They allow you to setup fixtures
for each test, often in the ``setUp`` method of your test in a very fast and
efficient manner.

"""
import factory

from mpass.models import Example


class ExampleFactory(factory.Factory):
  FACTORY_FOR = Example

  text = 'Foobar'


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

