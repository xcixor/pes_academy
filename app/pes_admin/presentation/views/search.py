from itertools import chain
from django.contrib.postgres.search import SearchVector
from django.views.generic import View, ListView, FormView
from django import forms
from django.utils.translation import gettext_lazy as _
from application.models import Application


class GetSearchApplicationsView(ListView):

    template_name = 'pes_admin/view_applications.html'
    model = Application
    context_object_name = 'applications'
    paginate_by = 50
    partial_template_name = 'pes_admin/snippets/view_applications.html'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        search_fields = SearchVector('application_creator__email') \
            + SearchVector('application_creator__username') \
            + SearchVector('application_creator__full_name') \
            + SearchVector('application_creator__id') + \
            SearchVector('stage') + SearchVector('slug')
        query = self.kwargs.get('search', None)
        query = self.request.session.get('search', None)
        if query:
            full_search = queryset.annotate(
                search=search_fields
            ).filter(search=query)
            partial_search = queryset.annotate(
                search=search_fields
            ).filter(search__icontains=query)
            search_results = list(chain(full_search, partial_search))
            search_results = list(set(search_results))
            queryset = search_results
        return queryset

    def get_template_names(self):
        if self.request.htmx:
            return self.partial_template_name
        return self.template_name


class SearchForm(forms.Form):

    default_errors = {
        'required': 'Search field should not be empty',
        'invalid': 'Enter a valid value'
    }

    search = forms.CharField(error_messages=default_errors)

    def clean_search(self):
        search = self.cleaned_data['search']
        if not search:
            search_error_message = _(
                'Search field should not be empty')
            raise forms.ValidationError(search_error_message)
        return search


class PostSearchApplicationsView(FormView):

    form_class = SearchForm
    success_url = '/CgDX4znLdQDLFw/advanced/search/'
    template_name = 'pes_admin/view_applications.html'
    partial_template_name = 'pes_admin/snippets/view_applications.html'

    def form_valid(self, form):
        self.request.session['search'] = form.cleaned_data['search']
        return super().form_valid(form)

    def form_invalid(self, form):
        self.request.session.pop('sort', None)
        self.request.session.pop('search', None)
        return super().form_invalid(form)

    def get_template_names(self):
        if self.request.htmx:
            return self.partial_template_name
        return self.template_name


class SearchApplicationsView(View):

    def get(self, request, *args, **kwargs):
        view = GetSearchApplicationsView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostSearchApplicationsView.as_view()
        return view(request, *args, **kwargs)
