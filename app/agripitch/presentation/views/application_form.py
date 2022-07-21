from django.views.generic import DetailView
from agripitch.models import Competition


class ApplicationFormView(DetailView):

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
