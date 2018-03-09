
# -*- coding: utf-8 -*-

import logging
from django.contrib.auth.backends import ModelBackend
from django.utils.text import slugify
from dreamuserdb.models import User, Organisation, Role

LOG = logging.getLogger(__name__)

# Example response from mpass
# {
#   "username": "MPASSOID.0f5bf6ac4c8b5fa9f4587",
#   "first_name": "First",
#   "last_name": "Last",
#   "roles": [],
#   "attributes": [
#     {
#       "name": "source_name",
#       "value": "abc123"
#     }
#    ],
#   "external_id": "abc123"
# }


# Attributes from MPASS IdP
#MPASS-OID: MPASSOID.3660b479a4d5c65f93744
#MPASS-givenName: Test
#MPASS-group: vieras;Saa7;opettajat;8ab b-ruotsi;tino-testaa-2015-10-08;7a
#MPASS-municipality: Kauniainen
#MPASS-role: teacher
#MPASS-school: Kasavuoren Koulu
#MPASS-surname: Opettaja

class MPASSBackend(ModelBackend):
  source = u'mpass'

  def get_user_obj(self, user_data):
    return User.objects.get(username=user_data['HTTP_MPASS_OID'])

  def create_user_obj(self, user_data):
    return User(
      first_name=user_data['HTTP_MPASS_GIVENNAME'] or u'',
      last_name=user_data['HTTP_MPASS_SURNAME'] or u'',
      username=user_data['HTTP_MPASS_OID']
    )

  def update_user_obj(self, user, user_data):
    user.first_name = user_data['HTTP_MPASS_GIVENNAME'] or u''
    user.last_name = user_data['HTTP_MPASS_SURNAME'] or u''
    return user

  def get_organisation(self, user_data):
    # get an Organisation objects based on user data, creating if necessary
    org_title = user_data['HTTP_MPASS_MUNICIPALITY']
    org_name = slugify(org_title)
    try:
      return Organisation.objects.get(name=org_name, source=self.source)
    except Organisation.DoesNotExist:
      org_obj = Organisation.objects.create(name=org_name, title=org_title, source=self.source)
      LOG.info('New organisation created', extra={'data': {'org_obj': repr(org_obj)}})
      return org_obj

  def get_roles(self, organisation, user_data):
    # get a list of roles in organisation user has
    # currently MPASS only provides one, but it can change
    role_name = user_data['HTTP_MPASS_ROLE'] or 'student'
    try:
      return [Role.objects.get(organisation=organisation, name=role_name)]
    except Role.DoesNotExist:
      return [Role.objects.create(organisation=organisation, name=role_name, title=role_name, source=self.source, official=True)]

  def get_groups(self, organisation, user_data):
    # return groups for user
    # groups = user_data['HTTP_MPASS_GROUP'].split(';')
    return []

  def authenticate(self, **credentials):
    if 'request_meta' not in credentials:
      LOG.debug('request_meta not in credentials')
      return None

    if 'HTTP_MPASS_OID' not in credentials['request_meta']:
      LOG.debug('No HTTP_MPASS_OID in request.META. Check shibboleth')
      return None
    elif credentials['request_meta']['HTTP_MPASS_OID'] == '':
      LOG.debug('No HTTP_MPASS_OID in request.META. Check shibboleth')
      return None

    oid = credentials['request_meta']['HTTP_MPASS_OID']
    user_data = {}
    keys = [
        'HTTP_AUTHENTICATOR',
        'HTTP_AUTHNID',
        'HTTP_MPASS_OID',
        'HTTP_MPASS_GIVENNAME',
        'HTTP_MPASS_SURNAME',
        'HTTP_MPASS_GROUP',
        'HTTP_MPASS_ROLE',
        'HTTP_MPASS_STRUCTUREDROLE',
        'HTTP_MPASS_SCHOOL',
        'HTTP_MPASS_MUNICIPALITY',
        'HTTP_SHIB_AUTHENTICATION_METHOD',
    ]
    for k in keys:
      value = credentials['request_meta'].get(k, None)
      if value is not None:
        value = unicode(value.decode('utf-8'))
      user_data[k] = value
    LOG.debug('Meta values from educloud', extra={'data': {'request_meta': credentials['request_meta']}})
    LOG.debug('User data from educloud',
        extra={'data': {'user_data': user_data, 'oid': oid}})

    user = None
    # 1. Check if we already have user with given OID
    try:
      user = self.get_user_obj(user_data)
      user = self.update_user_obj(user, user_data)
    except User.DoesNotExist:
      # Else we have a new user, lets create it
      user = self.create_user_obj(user_data)

    user.save()

    # Set organisation
    for o in user.organisations.filter(source=self.source):
      user.organisations.remove(o)
    organisation = self.get_organisation(user_data)
    user.organisations.add(organisation)

    # Set roles
    for r in user.roles.filter(organisation=organisation, source=self.source):
      user.roles.remove(r)
    user.roles.add(*self.get_roles(organisation, user_data))

    return user

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2


