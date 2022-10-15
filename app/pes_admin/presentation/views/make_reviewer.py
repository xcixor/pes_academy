from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.views import View
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from application.models import Application


User = get_user_model()


class MakeStaffReviewerView(View):

    model = User
    context_object_name = 'staff'

    def get(self, request, **kwargs):
        user_id = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)
        if not user:
            error_message = _(
                'user not found.')
            messages.add_message(
                self.request, messages.ERROR, error_message)
            return redirect('/accounts/login/')
        reviewers_group, created = Group.objects.get_or_create(
            name='reviewers')
        content_type = ContentType.objects.get_for_model(Application)
        permission, created = Permission.objects.get_or_create(
            codename='can_view_application',
            name='Can view application',
            content_type=content_type)
        reviewers_group.permissions.add(permission)
        user.groups.add(reviewers_group)
        user.is_reviewer = True
        user.save()
        success_message = _('Great, staff member ') + \
            str(user) + _(' can now review applications.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return redirect('/CgDX4znLdQDLFw/advanced/view/staff/')
