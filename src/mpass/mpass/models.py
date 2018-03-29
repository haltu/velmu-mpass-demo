
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from parler.models import TranslatableModel, TranslatedFields


class TimeStampedModel(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)

  class Meta:
    abstract = True


@python_2_unicode_compatible
class AuthenticationSource(TimeStampedModel, TranslatableModel):
    """MPASS authentication sources."""
    auth_id = models.CharField(max_length=128)
    icon_url = models.CharField(max_length=2048, blank=True, null=True)
    tags = models.ManyToManyField('AuthenticationTag', blank=True)
    translations = TranslatedFields(
      title=models.CharField(max_length=2048)
    )

    @property
    def shib_auth_selection_parameter(self):
      return 'authnContextClassRef=urn:mpass.id:authnsource:%s' % self.auth_id

    def __str__(self):
        return self.auth_id


@python_2_unicode_compatible
class AuthenticationTag(TimeStampedModel, TranslatableModel):
    """MPASS authentication tags used for grouping AuthenticationSources."""
    tag_id = models.CharField(max_length=128)
    translations = TranslatedFields(
      title=models.CharField(max_length=2048)
    )

    @property
    def shib_auth_selection_parameter(self):
      return 'authnContextClassRef=urn:mpass.id:authntag:%s' % self.auth_id

    def __str__(self):
        return self.tag_id


@python_2_unicode_compatible
class Service(TimeStampedModel, TranslatableModel):
    """MPASS Service."""
    service_id = models.CharField(max_length=128)
    icon_url = models.CharField(max_length=2048, blank=True, null=True)
    service_url = models.CharField(max_length=2048, blank=True, null=True)
    sso_url = models.CharField(max_length=2048, blank=True, null=True)
    translations = TranslatedFields(
      description=models.CharField(max_length=2048),
      title=models.CharField(max_length=2048)
    )

    def __str__(self):
        return self.service_id

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

