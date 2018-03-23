
# -*- coding: utf-8 -*-

from dreamcards.models import UserGroup
from mpass.authbackends import MPASSBackend


class VelmuMPASSBackend(MPASSBackend):
  def configure_user(self, user, user_data):
    dreamcards_groups = []
    for mpass_role in self._parse_roles(user_data['MPASS_ROLE']):
      group_name = mpass_role.group
      try:
        dreamcards_groups.append(UserGroup.objects.get(name=group_name))
      except UserGroup.DoesNotExist:
        dreamcards_groups.append(UserGroup.objects.create(name=group_name))
    user.usergroups.set(dreamcards_groups)
    return user


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

