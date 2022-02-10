from django.contrib.auth.views import LoginView
from django.conf import settings
from django.contrib import messages


class UserLoginView(LoginView):

    template_name = "registration/login.html"

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        success_message = (
            f'Welcome back {self.request.user.username}!')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        next_url = self.request.GET.get("next", None)
        print(next_url)
        if next_url is None:
            return settings.LOGIN_REDIRECT_URL
        return next_url