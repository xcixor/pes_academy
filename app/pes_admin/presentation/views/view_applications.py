from itertools import chain
from django.contrib.postgres.search import SearchVector
from django.views.generic import ListView
from application.models import Application


class ApplicationsView(ListView):

    template_name = 'pes_admin/view_applications.html'
    partial_template_name = 'pes_admin/snippets/view_applications.html'
    model = Application
    context_object_name = 'applications'
    paginate_by = 50

    def get(self, request, *args, **kwargs):
        sort_term = self.request.GET.get('stage')
        if sort_term:
            self.request.session['sort'] = sort_term
        search_term = self.request.GET.get('search')
        if search_term:
            self.request.session['search'] = search_term
        return super().get(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        sort_term = self.request.session.get('sort', None)
        stages = ['step_one', 'step_two', 'step_three', 'step_four']
        if sort_term in stages:
            queryset = queryset.filter(stage=sort_term)
        search_fields = SearchVector('application_creator__email') \
            + SearchVector('application_creator__username') \
            + SearchVector('application_creator__full_name') \
            + SearchVector('application_creator__id') + \
            SearchVector('stage') + SearchVector('slug')
        search_query = self.request.session.get('search', None)
        if search_query:
            full_search = queryset.annotate(
                search=search_fields
            ).filter(search=search_query)
            partial_search = queryset.annotate(
                search=search_fields
            ).filter(search__icontains=search_query)
            search_results = list(chain(full_search, partial_search))
            search_results = list(set(search_results))
            queryset = search_results
        return queryset

    def get_template_names(self):
        if self.request.htmx:
            return self.partial_template_name
        return self.template_name
