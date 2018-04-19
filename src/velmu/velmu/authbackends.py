
# -*- coding: utf-8 -*-

import uuid
from dreamcards.models import UserGroup
from dreamsso.models import User as SSOUser
from dreamuserdb.models import Service, ServicePermission, User
from mpass.authbackends import MPASSBackend
from velmu import settings


class VelmuMPASSBackend(MPASSBackend):
  def get_user_obj(self, user_data):
    mpass_uid = user_data['HTTP_MPASS_UID']
    if mpass_uid in settings.PERSISTENT_ACCOUNTS:
      return User.objects.get(username=mpass_uid)
    # public demo credentials always create new accounts when logging in
    return User(
      first_name=user_data['HTTP_MPASS_GIVENNAME'] or u'',
      last_name=user_data['HTTP_MPASS_SN'] or u'',
      username='demo/%s' % uuid.uuid4(),
      external_id=mpass_uid,
    )

  def configure_role(self, role, _user_data):
    # Add card sharing permission
    permission, _created = ServicePermission.objects.get_or_create(
      name='dreamcards',
      entity='dreamcards',
      action='can_share_cards',
      service=self.get_service(),
    )
    role.permissions.add(permission)
    return role

  def get_service(self):
    service, _created = Service.objects.get_or_create(
      name='app',
      defaults={'title': 'app'},
    )
    return service

  def get_user(self, pk):
    # Django authentication middleware populates request.user
    # using this method
    return SSOUser.objects.get(pk=pk)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

