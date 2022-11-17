from itertools import chain
from django.contrib.postgres.search import SearchVector
from django.views.generic import ListView
from application.models import Application, ApplicationReview


class FloatingCompletedApplications(ListView):

    model = Application
    template_name = 'pes_admin/unassigned_applications.html'
    partial_template_name = 'pes_admin/snippets/unassigned_applications.html'
    context_object_name = 'applications'
    paginate_by = 50

    def get(self, request, *args, **kwargs):
        search_term = self.request.GET.get('search')
        if search_term:
            self.request.session['search'] = search_term
        return super().get(request, *args, **kwargs)

    def get_template_names(self):
        if self.request.htmx:
            return self.partial_template_name
        return self.template_name

    def get_queryset(self):
        queryset = super().get_queryset()
        floating_un_disqualified = queryset.filter(
            is_in_review=True,
        )
        disqualified = queryset.filter(
            disqualified=True,
        )
        applications_in_reviews_ids = ApplicationReview.objects.all(
        ).values_list('application__id', flat=True)
        floating_ids = []
        for application in floating_un_disqualified:
            if application.id not in applications_in_reviews_ids:
                floating_ids.append(application.id)
        for application in disqualified:
            if application.id not in applications_in_reviews_ids:
                floating_ids.append(application.id)
        floating_applications = Application.objects.filter(id__in=floating_ids)
        search_fields = SearchVector('application_creator__email') \
            + SearchVector('application_creator__username') \
            + SearchVector('application_creator__full_name') \
            + SearchVector('application_creator__id') + \
            SearchVector('stage') + SearchVector('slug')
        search_query = self.request.session.get('search', None)
        if search_query:
            full_search = floating_applications.annotate(
                search=search_fields
            ).filter(search=search_query)
            partial_search = floating_applications.annotate(
                search=search_fields
            ).filter(search__icontains=search_query)
            search_results = list(chain(full_search, partial_search))
            search_results = list(set(search_results))
            floating_applications = search_results
        return floating_applications
