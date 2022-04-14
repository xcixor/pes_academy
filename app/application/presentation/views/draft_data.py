from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse, HttpResponseNotFound
from django.utils.translation import gettext_lazy as _
from common.utils.common_queries import get_application
from application.services import set_draft_application_data_to_redis_cache


class DraftUserDataView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.META.get(
            'HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        draft = request.session.get('application_form_draft', None)
        if not draft:
            request.session['application_form_draft'] = {}
        for key, value in request.POST.items():
            request.session['application_form_draft'][key] = value
        request.session.modified = True
        data = request.session['application_form_draft']
        application, msg = get_application(request.user)
        not_found_msg = _('Not found')
        try:
            set_draft_application_data_to_redis_cache(application.id, data)
        except Exception as e:
            print(e)
            if is_ajax:
                return JsonResponse(
                    {}, status=400)
            return HttpResponseNotFound(not_found_msg)
        if is_ajax:
            return JsonResponse(
                data, status=201)
        return HttpResponseNotFound(not_found_msg)
