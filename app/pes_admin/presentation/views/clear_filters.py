from django.urls import reverse
from django_htmx.http import HttpResponseClientRedirect
from django.views.generic import View


class ClearSortView(View):

    template_name = 'pes_admin/view_applications.html'

    def get(self, request, *args, **kwargs):
        self.request.session.pop('sort', None)
        return HttpResponseClientRedirect(
            '/CgDX4znLdQDLFw/advanced/applications/all/')


class ClearSearchView(View):

    template_name = 'pes_admin/view_applications.html'

    def get(self, request, *args, **kwargs):
        self.request.session.pop('search', None)
        url_origin = request.META.get("HTTP_REFERER")
        if '/applications/unassigned/' in url_origin:
            return HttpResponseClientRedirect(
                '/CgDX4znLdQDLFw/advanced/applications/unassigned/')
        return HttpResponseClientRedirect(
                '/CgDX4znLdQDLFw/advanced/applications/all/')
