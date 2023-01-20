from django.views.generic import ListView
from django.contrib.auth import get_user_model
from itertools import chain
from django.contrib.postgres.search import SearchVector

User = get_user_model()


class AllUsersView(ListView):

    template_name = 'pes_admin/users_all.html'
    model = User
    context_object_name = 'users'
    paginate_by = 50

    def get_queryset(self):
        return super().get_queryset().filter(is_staff=False)


class RegularUsers(ListView):

    template_name = 'pes_admin/users_regular.html'
    model = User
    context_object_name = 'users'
    paginate_by = 50

    def get_queryset(self):
        return super().get_queryset().filter(
            is_applying_for_a_call_to_action=False)


class CallToActionUsers(ListView):

    template_name = 'pes_admin/users_call_to_action.html'
    partial_template_name = 'pes_admin/snippets/users_call_to_action.html'
    model = User
    context_object_name = 'users'
    paginate_by = 50

    def get(self, request, *args, **kwargs):
        search_term = self.request.GET.get('search')
        if search_term:
            self.request.session['search'] = search_term
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            is_applying_for_a_call_to_action=True)
        search_fields = SearchVector('username') \
            + SearchVector('email') \
            + SearchVector('full_name')
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
