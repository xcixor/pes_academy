from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.views.generic import DetailView
from django.urls import reverse
from common.utils.common_queries import get_application
from application.models import CallToAction, Application


class GetApplicationFormView(DetailView):

    template_name = 'agripitch/application_form.html'
    model = CallToAction
    context_object_name = 'competition'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shortlists = [
            shortlist for shortlist in self.get_object().shortlists.all()]
        criteria_items = []
        for shortlist in shortlists:
            for item in shortlist.criteria.all():
                criteria_items.append(item)
        context.update({'criteria': criteria_items})

        user = self.request.user
        application, msg = get_application(user)
        if not application:
            Application.objects.create(
                application_creator=user,
                call_to_action=self.get_object()
            )
        context['application'] = application
        return context


class PostApplicationFormView(SingleObjectMixin, View):

    model = CallToAction

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return redirect(
            reverse(
                'agripitch:application',
                kwargs={'slug': self.object.slug}))


class ApplicationFormView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        view = GetApplicationFormView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostApplicationFormView.as_view()
        return view(request, *args, **kwargs)
