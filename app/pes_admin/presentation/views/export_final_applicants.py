import csv
from datetime import datetime
from django.http import HttpResponse
from agripitch.models import Application

def get_csv_data():
    csv_data = []
    applications = Application.objects.filter(is_in_review=True)
    for application in applications:
          application_data = []
          application_data.append(application.application_creator.email)
          csv_data.append(application_data)
    return csv_data


def export_final_applicants(request):
    time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="all_review_applicants_{time}.csv"'
    writer = csv.writer(response)
    writer.writerow(["All applicants"])
    data = get_csv_data()
    for item in data:
        writer.writerow([item[0]])
    return response
