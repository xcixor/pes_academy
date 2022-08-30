from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from accounts.tokens import account_activation_token


class AccountActivationView(View):

    def get(self, request, *args, **kwargs):
        uidb64 = kwargs.pop('uidb64')
        token = kwargs.pop('token')
        user_model = get_user_model()
        user = user_model.objects.get_user_by_uid(uidb64)
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            piece_one = _('Congratulations ')
            piece_two = _(
                ', your account is now active!')
            success_message = piece_one + user.username + piece_two
            messages.add_message(
                request, messages.SUCCESS, success_message)
            login(request, user)
            return redirect('/')
        error_message = _('Uh oh! something went wrong.')
        messages.add_message(
            request, messages.SUCCESS, error_message)
        return render(request, 'registration/account_activation_invalid.html')


class ActivationEmailSentView(TemplateView):

    template_name = 'registration/activation_email_sent.html'
