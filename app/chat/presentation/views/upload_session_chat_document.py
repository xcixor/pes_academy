from django.http import JsonResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from chat.models import SessionChatHistory


class JsonableResponseMixin:
    """
    Mixin to add JSON support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        is_ajax = self.request.META.get(
            'HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        if is_ajax:
            return JsonResponse(form.errors, status=400)
        return JsonResponse({'errors': form.errors}, status=201)

    def form_valid(self, form):
        is_ajax = self.request.META.get(
            'HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        document = form.save(self.request)
        self.application = form.cleaned_data['application']
        if is_ajax:
            data = {
                'message': _('Success') + document.document_name + _(' has been saved!')
            }
            return JsonResponse(data, status=201)
        return super().form_valid(form)


class PostSessionFileView(LoginRequiredMixin, JsonableResponseMixin, CreateView):

    model = SessionChatHistory
    template_name = 'chat/room.html'
    fields = ['session', 'user', 'file', 'timestamp', 'type']

    def get_success_url(self) -> str:
        return reverse('chat:room')
