from django.views.generic import FormView
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render
from accounts.forms import (
    UserPasswordChangeForm, UserPasswordResetForm)


class PasswordChangeView(FormView):

    form_class = UserPasswordChangeForm
    template_name = 'password/password_change.html'
    success_url = '/accounts/profile/edit/'

    def get_form(self):
        form_class = self.get_form_class()
        form = form_class(self.request.user, self.request.POST)
        return form

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        message = (
            'Congratulations, your password has been changed successfully.')
        messages.add_message(self.request, messages.SUCCESS, message)
        return super().form_valid(form)

    def form_invalid(self, form):
        message = (
            'Something went wrong, please check your form below.')
        messages.add_message(self.request, messages.ERROR, message)
        context = self.get_context_data()
        context['password_change_form'] = form
        return render(self.request, self.template_name, context)


class PasswordResetView(FormView):

    template_name = 'password/password_reset.html'
    form_class = UserPasswordResetForm
    success_url = '/accounts/password_reset/done/'

    def form_valid(self, form):
        form.send_email(self.request)
        return super().form_valid(form)
