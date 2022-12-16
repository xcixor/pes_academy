from django.views.generic import DetailView
from application.models import Application


class ShortListDetailView(DetailView):

    template_name = 'eligibility/shortlist_detail.html'
    model = Application
    context_object_name = 'application'
