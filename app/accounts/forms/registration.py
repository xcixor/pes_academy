import re
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.password_validation import validate_password
from common.utils.email import HtmlEmailMixin
from accounts.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings


User = get_user_model()


class RegistrationForm(forms.ModelForm, HtmlEmailMixin):

    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password1(self):
        password = self.cleaned_data['password1']
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

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Please make sure your passwords match.")
        return password2

    def send_account_activation_email(self, user, request):
        to_email = user.email
        subject = "Account Activation"
        from_email = settings.VERIFIED_EMAIL_USER
        current_site = get_current_site(request)
        context = {
            "email": user.email,
            'domain': current_site.domain,
            "protocol": request.scheme,
            'email_head': subject,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        }
        super().send_email(
            subject, None, from_email, [to_email],
            template='registration/email/account_activation.html',
            context=context)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
