from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from accounts.models import User


class ViewProfile(LoginRequiredMixin, TemplateView):

    template_name = 'profile/profile.html'


class EditProfile(LoginRequiredMixin, UpdateView):

    model = User
    fields = [
        'linked_in', 'avatar', 'bio', 'age',
        'full_name', 'gender', 'preferred_language']
    template_name = 'profile/edit.html'
    success_url = '/accounts/profile/'

    def form_invalid(self, form):
        error_message = _(
            'Oops, something went wrong, please check your details')
        messages.add_message(
            self.request, messages.ERROR, error_message)
        return super().form_invalid(form)

    def form_valid(self, form):
        success_message = _(
            'Great! your details have been saved')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return super().form_valid(form)
