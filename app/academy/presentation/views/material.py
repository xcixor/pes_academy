from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from academy.models import Session, SessionMaterial
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse
from common.utils.email import HtmlEmailMixin


class GetMaterialPageView(DetailView):

    template_name = 'staff/material.html'
    model = Session
    context_object_name: str = 'session'


class UploadMaterialView(CreateView, HtmlEmailMixin):

    template_name = 'staff/material.html'
    model = SessionMaterial
    fields = ['material_name', 'material', 'session']

    def post(self, request, *args, **kwargs):
        self.session = Session.objects.get(pk=kwargs['pk'])
        return super().post(request, *args, **kwargs)

    def get_success_url(self) -> str:
        success_message = _(
            'Great! the material has been saved.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        to_email = self.object.session.coachee.email
        from_email = settings.VERIFIED_EMAIL_USER
        message_piece_one = _('Hi, your coach uploaded a new material: ')
        message_piece_two = _(
            ' Please login to your account to view it, thank you.')
        email_message = f'{message_piece_one} {self.object.material_name} {message_piece_two}'
        subject = _('Session Material')
        context = {
            'message': email_message,
        }
        super().send_email(
            subject, None, from_email, [to_email],
            template='staff/email/material.html', context=context)
        return reverse('academy:session_details', kwargs={'pk': self.object.session.pk})

    def form_invalid(self, form):
        message = _(
            'Hmm! something went wrong, please try again.')
        messages.add_message(
            self.request, messages.ERROR, message)
        context = self.get_context_data()
        context['form'] = form
        context['session'] = self.session
        return self.render_to_response(context)
