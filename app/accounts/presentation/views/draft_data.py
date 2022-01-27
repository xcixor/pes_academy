from django.views import View
from django.http import JsonResponse, HttpResponseNotFound


class DraftUserDataView(View):

    def post(self, request):
        is_ajax = request.META.get(
            'HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        draft = request.session.get('application_form_draft', None)
        if not draft:
            request.session['application_form_draft'] = {}
        for key, value in request.POST.items():
            request.session['application_form_draft'][key] = value
        if is_ajax:
            return JsonResponse(
                request.session['application_form_draft'], status=201)
        return HttpResponseNotFound('Not found')
