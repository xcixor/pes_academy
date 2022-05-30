from django.contrib.auth import get_user_model
from django.views import View
from django.shortcuts import get_object_or_404
from common.utils.email import HtmlEmailMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class MakeStaffCoachView(View, HtmlEmailMixin):

    model = User
    context_object_name = 'coach'

    def get(self, request, **kwargs):
        user_id = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)
        user.is_coach = True
        user.save()
        success_message = _('Great, staff member ') + \
            str(user) + _(' can coach applicants.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        to_email = user.email
        subject = _(
            'Account upgraded to coach')
        from_email = settings.VERIFIED_EMAIL_USER
        context = {
            'email_head': subject
        }
        super().send_email(
            subject, None, from_email, [to_email],
            template='pes_admin/email/coach.html',
            context=context)
        return redirect('/admin/advanced/view/staff/')
