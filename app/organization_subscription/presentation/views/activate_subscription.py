from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from accounts.tokens import account_activation_token


class ActivateSubscriptionView(View):

    def get(self, request, *args, **kwargs):
        uidb64 = kwargs.pop('uidb64')
        token = kwargs.pop('token')
        user_model = get_user_model()
        user = user_model.objects.get_user_by_uid(uidb64)
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            success_message = (
                f'Congratulations {user}, your have joined your '
                'organization\'s workspace. Please register to continue!')
            messages.add_message(
                request, messages.SUCCESS, success_message)
            return redirect('/accounts/register/')
        error_message = ('Uh oh! something went wrong.')
        messages.add_message(
            request, messages.SUCCESS, error_message)
        return render(request, 'registration/account_activation_invalid.html')
