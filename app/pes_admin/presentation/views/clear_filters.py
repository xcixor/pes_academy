from django.urls import reverse
from django_htmx.http import HttpResponseClientRedirect
from django.views.generic import View


class ClearSortView(View):

    template_name = 'pes_admin/view_applications.html'

    def get(self, request, *args, **kwargs):
        self.request.session.pop('sort', None)
        url_origin = request.META.get("HTTP_REFERER")
        if '/users/call-to-action/' in url_origin:
            return HttpResponseClientRedirect(
                '/CgDX4znLdQDLFw/advanced/users/call-to-action/')
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
        if '/users/call-to-action/' in url_origin:
            return HttpResponseClientRedirect(
                '/CgDX4znLdQDLFw/advanced/users/call-to-action/')
        return HttpResponseClientRedirect(
            '/CgDX4znLdQDLFw/advanced/applications/all/')
