import xlwt
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Cast
from django.db.models import CharField
from accounts.models import User


def export_inactive_user_emails_to_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="dormant_accounts.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Dormant Accounts')

    # Sheet header, first row
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    font_style.alignment.wrap = 1
    header = ('Dormant Accounts')
    ws.write_merge(0, 0, 0, 5, header, font_style)

    # question title headings
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Email', 'Date joined']
    row_num = 1
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    style = xlwt.XFStyle()
    style.alignment.wrap = 1

    cast_expr = Cast('date_joined', output_field=CharField())
    rows = User.objects.annotate(dt_as_str=cast_expr).values_list(
        'email', 'dt_as_str')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], style)
    wb.save(response)
    return response
