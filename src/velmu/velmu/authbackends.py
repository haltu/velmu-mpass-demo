
# -*- coding: utf-8 -*-

from dreamcards.models import UserGroup
from dreamsso.models import User
from dreamuserdb.models import Service, ServicePermission
from mpass.authbackends import MPASSBackend


class VelmuMPASSBackend(MPASSBackend):
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
    return User.objects.get(pk=pk)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

