from django.views import View
from django.http import JsonResponse, HttpResponseNotFound
from django.utils.translation import gettext_lazy as _
from agripitch.models import SubCriteriaItem, Application


class DeleteSubCriteriaView(View):

    def post(self, request):
        is_ajax = request.META.get(
            'HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        label = request.POST.get('label')
        # application = request.POST.get('application')
        try:
            item = SubCriteriaItem.objects.get(
                label=label)
            if item.type == 'file':
                item.sub_criteria_item_documents.filter(
                    application=request.user.application).delete()
            else:
                item.responses.filter(
                    application=request.user.application).delete()

        except SubCriteriaItem.DoesNotExist as e:
            print(e)
        not_found_msg = _('Not found')
        if is_ajax and item:
            return JsonResponse(
                {}, status=204)
        else:
            return JsonResponse(
                {}, status=400)
        return HttpResponseNotFound(not_found_msg)
