import csv
from datetime import datetime
from django.http import HttpResponse
from agripitch.models import CriteriaItem, Application


def get_csv_data():
    csv_data = []
    for application in Application.objects.all():
        if application.stage == 'step_one':
            application_data = []
            application_data.append(application.application_creator.email)
            application_existing_criterias = [
                response.sub_criteria_item.criteria.id for response in application.responses.all()]
            application_existing_criterias = [
                *set(application_existing_criterias)]
            remaining_criteria = CriteriaItem.objects.all().exclude(
                id__in=application_existing_criterias).values_list('label', flat=True)
            application_data.append(list(remaining_criteria))
            csv_data.append(application_data)
    return csv_data


def export_remaining_steps_for_users(request):
    time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="remaining_steps_{time}.csv"'
    writer = csv.writer(response)
    writer.writerow(["Remaining Steps for Each User"])
    data = get_csv_data()
    for item in data:
        writer.writerow([item[0], item[1]])
    return response
