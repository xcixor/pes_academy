import re
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from common.utils.email import HtmlEmailMixin

User = get_user_model()


class UserPasswordChangeForm(PasswordChangeForm):

    def clean_new_password1(self):
        password = self.cleaned_data['new_password1']
        validate_password(password)
        self.custom_validate_password(password)
        return password

    def custom_validate_password(self, password):
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if not regex.search(password):
            no_special_characters_error_message = _(
                "Your password should have a special character.")
            raise forms.ValidationError(no_special_characters_error_message)
        if not any(i.isdigit() for i in password):
            no_digit_error_message = _(
                "Your password should have at least one number.")
            raise forms.ValidationError(no_digit_error_message)
        return password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            passwords_dont_match_error_message = _(
                "Please make sure your passwords match.")
            raise forms.ValidationError(passwords_dont_match_error_message)
        return new_password2


class UserPasswordResetForm(PasswordResetForm, HtmlEmailMixin):

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            return user.email
        except ObjectDoesNotExist:
            piece_one = _("Sorry, account with the email")
            piece_two = _("does not exist.")
            message = f"{piece_one} {email} {piece_two}"
            raise forms.ValidationError(message)

    def send_email(self, request):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            subject = _("Password Reset Requested")
            from_email = settings.VERIFIED_EMAIL_USER
            current_site = get_current_site(request)
            context = {
                "email": user.email,
                'domain': current_site.domain,
                "protocol": request.scheme,
                'site_name': 'Website',
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'token': default_token_generator.make_token(user)
            }
            super().send_email(
                subject, None, from_email, [email],
                template='password/email/password_reset_email.html',
                context=context)
        except ObjectDoesNotExist:
            piece_one = _("Sorry, account with the email")
            piece_two = _("does not exist.")
            message = f"{piece_one} {email} {piece_two}"
            raise forms.ValidationError(message)
