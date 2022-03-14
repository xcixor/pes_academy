from django.views.generic import CreateView
from django.contrib import messages
from application.models import ApplicationDocument


class UploadExtraDocuments(CreateView):

    model = ApplicationDocument
    fields = '__all__'
    success_url = '/accounts/dashboard/'
    template_name = "profile/dashboard.html"

    def get_success_url(self):
        success_message = (
            f'Great, {self.object.document_name} has been '
            'successfully uploaded.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return super().get_success_url()

    def form_invalid(self, form):
        print(form.errors)
        error_message = (
            'Hmm something went wrong please check the errors '
            'in the form below.')
        messages.add_message(
            self.request, messages.ERROR, error_message)
        return super().form_invalid(form)
