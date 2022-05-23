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
            raise forms.ValidationError(
                "Your password should have a special character.")
        if not any(i.isdigit() for i in password):
            raise forms.ValidationError(
                "Your password should have at least one number.")
        return password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError(
                "Please make sure your passwords match.")
        return new_password2


class UserPasswordResetForm(PasswordResetForm, HtmlEmailMixin):

    def send_email(self, request):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            subject = "Password Reset Requested"
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
            raise forms.ValidationError
