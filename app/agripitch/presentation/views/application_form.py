from django.shortcuts import redirect
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.views.generic import DetailView
from django.urls import reverse
from agripitch.models import Competition


class GetApplicationFormView(DetailView):

    template_name = 'agripitch/application_form.html'
    model = Competition
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
        return context


class PostApplicationFormView(SingleObjectMixin, View):

    model = Competition

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return redirect(
            reverse(
                'agripitch:application',
                kwargs={'slug': self.object.slug}))


class ApplicationFormView(View):

    def get(self, request, *args, **kwargs):
        view = GetApplicationFormView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostApplicationFormView.as_view()
        return view(request, *args, **kwargs)
