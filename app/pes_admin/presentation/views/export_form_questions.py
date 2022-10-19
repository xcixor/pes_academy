import xlwt

from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from agripitch.models import SubCriteriaItem, CriteriaItem


def export_agripitch_questions_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="agripitch_questions.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Questions')

    # Sheet header, first row
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    font_style.alignment.wrap = 1
    header = (
        'These are the updated questions \n'
        'Questions ending with * means they are required'
    )
    ws.write_merge(0, 0, 0, 5, header, font_style)

    # question title headings
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Question', 'Answer Type', 'Choices']
    row_num = 1
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    style = xlwt.XFStyle()
    style.alignment.wrap = 1

    rows = SubCriteriaItem.objects.all().values_list(
        'label', 'criteria__label')
    updated_rows = []
    for row in rows:
        object = SubCriteriaItem.objects.get(label=row[0])
        type = [object.get_type_display()]
        choices = object.choices.all()
        choice_list = [choice.choice + "\n" for choice in choices]
        updated_row = row + tuple(type) + tuple([choice_list])
        updated_rows.append(updated_row)

    criterias = [criteria.label for criteria in CriteriaItem.objects.all()]
    for criteria in range(len(criterias)):
        row_num += 1
        ws.write(row_num, 0, criterias[criteria], font_style)
        for row in list(filter(lambda c: c[1] == criterias[criteria], updated_rows)):
            row = row[:-3] + row[-2:]
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], style)
    wb.save(response)
    return response
