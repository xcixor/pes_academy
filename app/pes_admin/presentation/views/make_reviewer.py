from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.views import View
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from application.models import Application


User = get_user_model()


class MakeStaffReviewerView(View):

    # template_name = 'pes_admin/view_staff.html'
    model = User
    context_object_name = 'staff'

    def get(self, request, **kwargs):
        user_id = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)
        if not user:
            return redirect('/accounts/login/')
        reviewers_group, created = Group.objects.get_or_create(
            name='reviewers')
        content_type = ContentType.objects.get_for_model(Application)
        permission, created = Permission.objects.get_or_create(
            codename='can_view_project',
            name='Can view project',
            content_type=content_type)
        reviewers_group.permissions.add(permission)
        user.groups.add(reviewers_group)
        user.is_reviewer = True
        user.save()
        return redirect('/admin/advanced/view/staff/')
