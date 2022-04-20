from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class CreateModerator(UpdateView):

    model = User
    fields = ['is_moderator']
    success_url = '/admin/advanced/view/staff/'

    def get_success_url(self) -> str:
        success_message = _('Great, staff member ') + \
            self.object.username + _(' is now a moderator.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return super().get_success_url()
