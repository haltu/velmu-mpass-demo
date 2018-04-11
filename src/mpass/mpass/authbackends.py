
# -*- coding: utf-8 -*-

import logging
from collections import namedtuple
from django.contrib.auth.backends import ModelBackend
from django.utils.text import slugify
from dreamuserdb.models import User, Organisation, Role, Group

LOG = logging.getLogger(__name__)
MPASSRole = namedtuple('MPASSRole', 'org,school_code,group,role')


class MPASSBackend(ModelBackend):
  source = u'mpass'

  def get_user_obj(self, user_data):
    return User.objects.get(username=user_data['HTTP_MPASS_UID'])

  def create_user_obj(self, user_data):
    return User(
      first_name=user_data['HTTP_MPASS_GIVENNAME'] or u'',
      last_name=user_data['HTTP_MPASS_SN'] or u'',
      username=user_data['HTTP_MPASS_UID']
    )

  def update_user_obj(self, user, user_data):
    user.first_name = user_data['HTTP_MPASS_GIVENNAME'] or u''
    user.last_name = user_data['HTTP_MPASS_SN'] or u''
    return user

  def get_organisation(self, user_data):
    # get an Organisation objects based on user data, creating if necessary
    org_title = user_data['HTTP_MPASS_MUNICIPALITY']
    org_name = user_data['HTTP_MPASS_MUNICIPALITYCODE']
    try:
      return Organisation.objects.get(name=org_name, source=self.source)
    except Organisation.DoesNotExist:
      org_obj = Organisation.objects.create(name=org_name, title=org_title, source=self.source)
      LOG.info('New organisation created', extra={'data': {'org_obj': repr(org_obj)}})
      return org_obj

  def get_roles(self, organisation, user_data):
    roles = []
    for mpass_role in self._parse_roles(user_data['HTTP_MPASS_ROLE']):
      role_name = mpass_role.role
      try:
        role = Role.objects.get(organisation=organisation, name=role_name)
      except Role.DoesNotExist:
        role = Role.objects.create(organisation=organisation, name=role_name, title=role_name, source=self.source, official=True)
      role = self.configure_role(role, user_data)
      roles.append(role)
    return roles

  def configure_role(self, role, user_data):
    return role

  def _parse_roles(self, mpass_role_str):
    # mpass_roles is a list of MPASSRole named tuples
    return map(lambda x: MPASSRole._make(x.split('|')), mpass_role_str.replace(r'\;', '|').split(';'))

  def get_groups(self, organisation, user_data):
    groups = []
    for mpass_role in self._parse_roles(user_data['HTTP_MPASS_ROLE']):
      group_name = mpass_role.group
      try:
        groups.append(Group.objects.get(organisation=organisation, name=group_name))
      except Group.DoesNotExist:
        groups.append(Group.objects.create(organisation=organisation, name=group_name, title=group_name, source=self.source, official=True))
    return groups

  def authenticate(self, **credentials):
    if 'request_meta' not in credentials:
      LOG.debug('request_meta not in credentials')
      return None

    if 'HTTP_MPASS_UID' not in credentials['request_meta']:
      LOG.debug('No HTTP_MPASS_UID in request.META. Check shibboleth')
      return None
    elif credentials['request_meta']['HTTP_MPASS_UID'] == '':
      LOG.debug('No HTTP_MPASS_UID in request.META. Check shibboleth')
      return None

    uid = credentials['request_meta']['HTTP_MPASS_UID']
    user_data = {}
    keys = [
      'HTTP_MPASS_CLASS',
      'HTTP_MPASS_CLASSLEVEL',
      'HTTP_MPASS_CURRENTGIVENNAME',
      'HTTP_MPASS_GIVENNAME',
      'HTTP_MPASS_LEGACYCRYPTID',
      'HTTP_MPASS_LEGACYCRYPTIDE',
      'HTTP_MPASS_MUNICIPALITY',
      'HTTP_MPASS_MUNICIPALITYCODE',
      'HTTP_MPASS_ROLE',
      'HTTP_MPASS_SCHOOL',
      'HTTP_MPASS_SCHOOLCODE',
      'HTTP_MPASS_SN',
      'HTTP_MPASS_UID',
    ]
    for k in keys:
      value = credentials['request_meta'].get(k, None)
      if value is not None:
        value = unicode(value.decode('utf-8'))
      user_data[k] = value
    LOG.debug('User data from educloud',
        extra={'data': {'user_data': user_data, 'uid': uid}})

    user = None
    # Check if we already have user with given uid
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

    # Set groups
    for g in user.user_groups.filter(organisation=organisation, source=self.source):
      user.user_groups.remove(g)
    user.user_groups.add(*self.get_groups(organisation, user_data))

    user = self.configure_user(user, user_data)
    return user

  def configure_user(self, user, user_data):
    return user

  def get_user(self, pk):
    # Django authentication middleware populates request.user
    # using this method
    return User.objects.get(pk=pk)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2


