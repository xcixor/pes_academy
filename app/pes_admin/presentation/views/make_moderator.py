from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from application.models import Application


User = get_user_model()


class CreateModerator(UpdateView):

    model = User
    fields = ['is_moderator']
    success_url = '/CgDX4znLdQDLFw/advanced/view/staff/'

    def get_success_url(self) -> str:
        reviewers_group, created = Group.objects.get_or_create(
            name='reviewers')
        content_type = ContentType.objects.get_for_model(Application)
        permission, created = Permission.objects.get_or_create(
            codename='can_view_application',
            name='Can view application',
            content_type=content_type)
        reviewers_group.permissions.add(permission)
        self.object.groups.add(reviewers_group)
        self.object.is_reviewer = True
        self.object.save()

        success_message = _('Great, staff member ') + \
            self.object.username + _(' is now a moderator.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return super().get_success_url()
