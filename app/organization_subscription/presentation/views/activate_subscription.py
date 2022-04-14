from django.views import View
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class ActivateSubscriptionView(View):

    def get(self, request, *args, **kwargs):
        success_message = _(
            'Congratulations, your have joined your '
            'organization\'s workspace. Please register to continue!')
        messages.add_message(
            request, messages.SUCCESS, success_message)
        return redirect('/accounts/register/')
