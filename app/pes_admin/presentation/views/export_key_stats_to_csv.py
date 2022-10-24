import csv
from django.http import HttpResponse
from pes_admin.templatetags.admin_extras import (
    get_total_afdb_applicants, get_total_applications,
    get_total_applications_by_criteria, get_applications_by_stage)


def recursive1(index, rows):
    if index == len(rows):
        print(f'I have {index} cake(s).')
        return True
    print(f'I have {index} cake(s).')
    index += 1
    return recursive1(index, rows)


def get_number(n=0, rows=[]):
    column = ""
    while n < len(rows):
        for i in range(0, len(rows)):
            print(i)
            n += 1
            column = f'{rows[i][0]}({rows[i][1]})'
            get_number(n, rows)
    if n < len(rows):
        return get_number(n, rows)
    return column


def export_key_stats_to_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="key_stats.csv"'
    writer = csv.writer(response)
    writer.writerow(
        [f'Total AfDB Applicants: {(get_total_afdb_applicants("").count())}'])
    writer.writerow(
        [f'Total Applications: {(get_total_applications(""))}'])
    applications_by_stage = get_applications_by_stage('')
    formatted_applications_by_stage = [
        f'{item[0]}({item[1]})' for item in applications_by_stage]
    writer.writerow(
        [
            'Application by Stage',
            formatted_applications_by_stage,
        ]
    )
    applications_by_country = get_total_applications_by_criteria('Country *')
    formatted_applications_by_country = [
        f'{item[0]}({item[1]})' for item in applications_by_country]
    writer.writerow(
        [
            'Application by Country',
            formatted_applications_by_country,
        ]
    )
    applications_by_gender = get_total_applications_by_criteria('Gender *')
    formatted_applications_by_gender = [
        f'{item[0]}({item[1]})' for item in applications_by_gender]
    writer.writerow(
        [
            'Application by Gender',
            formatted_applications_by_gender,
        ]
    )
    applications_by_language = get_total_applications_by_criteria('Language *')
    formatted_applications_by_language = [
        f'{item[0]}({item[1]})' for item in applications_by_language]
    writer.writerow(
        [
            'Application by Language',
            formatted_applications_by_language,
        ]
    )
    return response
