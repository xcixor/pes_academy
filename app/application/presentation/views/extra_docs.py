from django.views.generic import CreateView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from application.models import ApplicationDocument
from application.forms import ApplicationDocumentForm


class UploadExtraDocumentsView(CreateView):

    model = ApplicationDocument
    form_class = ApplicationDocumentForm
    success_url = '/accounts/dashboard/'
    template_name = "profile/dashboard.html"

    def get_success_url(self):
        msg_piece_one = _('Great, ')
        msg_piece_two = _(' has been successfully uploaded.')
        success_message = msg_piece_one + self.object.document_name + \
            msg_piece_two
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return super().get_success_url()

    def form_invalid(self, form):
        print(form.errors)
        error_message = _(
            'Hmm something went wrong please check the errors '
            'in the form below.')
        messages.add_message(
            self.request, messages.ERROR, error_message)
        return super().form_invalid(form)
