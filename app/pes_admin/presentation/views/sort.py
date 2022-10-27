from django.views.generic import ListView
from application.models import Application


class SortByStageView(ListView):

    template_name = 'pes_admin/view_applications.html'
    model = Application
    context_object_name = 'applications'
    paginate_by = 50
    partial_template_name = 'pes_admin/snippets/view_applications.html'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        sort_term = self.request.GET.get('stage')
        queryset = queryset.filter(stage=sort_term)
        self.request.session['sort'] = sort_term
        return queryset

    def get_template_names(self):
        if self.request.htmx:
            return self.partial_template_name
        return self.template_name
