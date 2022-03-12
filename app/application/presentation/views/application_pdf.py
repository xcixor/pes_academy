from django.views import View
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from application.forms import ApplicationForm
from common.utils.common_queries import get_application
from application.services.redis_caching import (
    get_draft_application_data_from_redis_cache)


class ApplicationPDFView(View):

    def get(self, request):
        user = self.request.user
        application, msg = get_application(user)
        form = ApplicationForm(request)
        data = get_draft_application_data_from_redis_cache(application.pk)
        context = {
            'form': form,
            'application': application,
            'data': data
        }
        html = render_to_string(
            'application/application_pdf.html', context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            f'filename=application_{application}.pdf')
        weasyprint.HTML(string=html).write_pdf(
            response,
            stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/application_pdf.css')])
        return response