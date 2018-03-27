
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

  def configure_user(self, user, user_data):
    # mutate user into a dreamsso.User
    user = User.objects.get(pk=user.pk)

    # add dreamcards groups for card sharing
    dreamcards_groups = []
    for mpass_role in self._parse_roles(user_data['HTTP_MPASS_ROLE']):
      group_name = mpass_role.group
      try:
        dreamcards_groups.append(UserGroup.objects.get(name=group_name))
      except UserGroup.DoesNotExist:
        dreamcards_groups.append(UserGroup.objects.create(name=group_name))
    user.usergroups.set(dreamcards_groups)
    return user

  def get_user(self, pk):
    # Django authentication middleware populates request.user
    # using this method
    return User.objects.get(pk=pk)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

