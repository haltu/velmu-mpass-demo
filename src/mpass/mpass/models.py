
# -*- coding: utf-8 -*-

"""
Models for the ``mpass`` application.

"""
from django.db import models


class Example(models.Model):
    """Example model class."""
    text = models.TextField(blank=True, null=True)


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

