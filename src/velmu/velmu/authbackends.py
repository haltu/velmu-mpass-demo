
# -*- coding: utf-8 -*-

from dreamcards.models import UserGroup
from dreamsso.models import User
from mpass.authbackends import MPASSBackend


class VelmuMPASSBackend(MPASSBackend):
  def configure_user(self, user, user_data):
    # mutate user into a dreamsso.User
    user = User.objects.get(pk=user.pk)
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
    return User.objects.get(pk=pk)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

