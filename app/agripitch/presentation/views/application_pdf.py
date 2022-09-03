from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from agripitch.models import CriteriaItem
from application.models import CallToAction


def generate_application_pdf(request):
    criteria = CriteriaItem.objects.all()
    context = {
        'criteria': criteria,
        'request': request,
        'call_to_action': CallToAction.objects.first()
    }
    html_string = render_to_string(
        'agripitch/pdf/application_form.html', context)
    # base_url=request.build_absolute_uri()
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    html.write_pdf(target='/tmp/application.pdf')

    fs = FileSystemStorage('/tmp')
    with fs.open('application.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="application.pdf"'
        return response

    return response
