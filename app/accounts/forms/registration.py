import re
from django.utils import timezone
from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from captcha.fields import ReCaptchaField
from common.utils.email import HtmlEmailMixin
from accounts.tokens import account_activation_token


User = get_user_model()

USER_TYPE_CHOICES = (
    (True, _('Applying for call to action')),
    (False, _('Other'))
)


class RegistrationForm(forms.ModelForm, HtmlEmailMixin):

    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    terms = forms.BooleanField(initial=False, required=True)
    is_applying_for_a_call_to_action = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        label=_("Reason for Application"),
        widget=forms.Select(
            attrs={
                'class': 'input-field'}),
        required=True)
    captcha = ReCaptchaField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'is_applying_for_a_call_to_action']

    def clean_password1(self):
        password = self.cleaned_data['password1']
        validate_password(password)
        self.custom_validate_password(password)
        return password

    def clean_terms(self):
        terms = self.cleaned_data['terms']
        if not terms:
            terms_error_message = _(
                'Please read and agree to our terms '
                'and privacy by checking the box')
            raise forms.ValidationError(terms_error_message)
        return terms

    def custom_validate_password(self, password):
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if not regex.search(password):
            raise forms.ValidationError(
                _("Your password should have a special character."))
        if not any(i.isdigit() for i in password):
            raise forms.ValidationError(
                _("Your password should have at least one number."))
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                _("Please make sure your passwords match."))
        return password2

    def send_account_activation_email(self, user, request):
        to_email = user.email
        subject = _("Welcome to Agripitch 2022! Please Confirm Your Email")
        from_email = settings.VERIFIED_EMAIL_USER
        current_site = get_current_site(request)
        context = {
            "username": user.username,
            "email": user.email,
            'domain': current_site.domain,
            "protocol": request.scheme,
            'email_head': subject,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        }
        return super().send_email(
            subject, None, from_email, [to_email],
            template='registration/email/account_activation.html',
            context=context)

    def notify_admin(self, user):
        subject = _(
            'New User Registration')
        from_email = settings.VERIFIED_EMAIL_USER
        to_email = settings.ADMIN_EMAILS
        context = {
            'email_address': user.email,
            'time': timezone.now()
        }
        return super().send_email(
            subject, None, from_email, to_email,
            template='registration/email/admin/new_user.html',
            context=context)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            self.notify_admin(user)
        return user


class ResendActivationEmail(forms.Form, HtmlEmailMixin):

    email = forms.EmailField(required=True)

    def get_account(self, email):
        existing_user = None
        try:
            existing_user = User.objects.get(email=email)
        except User.DoesNotExist as de:
            print(de)
        return existing_user

    def clean_email(self):
        email = self.cleaned_data.get("email")
        existing_user = self.get_account(email)
        if not existing_user:
            raise forms.ValidationError(
                _("Sorry that account does not exist."), code='invalid')
        if existing_user.is_active:
            raise forms.ValidationError(
                _(
                    'Your account is already active. '
                    'Please login with the details you registered with, '
                    'or reset your password'), code='invalid')
        return email

    def resend_account_activation_email(self, request):
        email = self.cleaned_data.get("email")
        user = self.get_account(email)
        if not user:
            raise forms.ValidationError(
                _("Sorry the account does not exist."), code='invalid')
        to_email = user.email
        subject = _("Welcome to Agripitch 2022! Please Confirm Your Email")
        from_email = settings.VERIFIED_EMAIL_USER
        current_site = get_current_site(request)
        context = {
            "username": user.username,
            "email": user.email,
            'domain': current_site.domain,
            "protocol": request.scheme,
            'email_head': subject,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        }
        return super().send_email(
            subject, None, from_email, [to_email],
            template='registration/email/account_activation.html',
            context=context)

    def notify_admin(self, user):
        subject = _(
            'New User Registration')
        from_email = settings.VERIFIED_EMAIL_USER
        to_email = settings.ADMIN_EMAILS
        context = {
            'email_address': user.email,
            'time': timezone.now()
        }
        return super().send_email(
            subject, None, from_email, to_email,
            template='registration/email/admin/new_user.html',
            context=context)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            self.notify_admin(user)
        return user
