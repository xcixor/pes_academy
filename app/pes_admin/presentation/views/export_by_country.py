import csv
from datetime import datetime
from django.http import HttpResponse
from agripitch.models import (
    Application, get_sub_criteria_item_response_if_exist)
from agripitch.utils import get_sub_criteria_item_by_label


def get_csv_data():
    csv_data = []
    non_unique_countries = []
    sub_criteria_item = get_sub_criteria_item_by_label('Country *')
    for application in Application.objects.all():
        if application.stage == 'step_two':
            country = get_sub_criteria_item_response_if_exist(
                sub_criteria_item, application)
            non_unique_countries.append(country.value)
    print(non_unique_countries)
    unique_countries = set(non_unique_countries)
    for country in unique_countries:
        count = non_unique_countries.count(country)
        csv_data.append([country, count])
    return csv_data


def export_applications_by_country(request):
    time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="countries_{time}.csv"'
    writer = csv.writer(response)
    data = get_csv_data()
    for item in data:
        writer.writerow([item[0], item[1]])
    return response
