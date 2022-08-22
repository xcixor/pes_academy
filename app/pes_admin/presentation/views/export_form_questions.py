import xlwt

from django.http import HttpResponse
from agripitch.models import SubCriteriaItem


def export_agripitch_questions_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="agripitch_questions.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Questions')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Question', 'Criteria', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = SubCriteriaItem.objects.all().values_list(
        'label', 'criteria__label')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
