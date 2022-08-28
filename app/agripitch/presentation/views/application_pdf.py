import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from agripitch.models import SubCriteriaItem, CriteriaItem


from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML


def generate_application_pdf(request):
    criteria = CriteriaItem.objects.all()
    context = {
        'criteria': criteria,
        'request': request
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
