import csv
from datetime import datetime
from django.http import HttpResponse
from accounts.models import User

def get_csv_data():
    csv_data = []
    reviewers = User.objects.filter(is_reviewer=True)
    reviewer_list = []
    for reviewer in reviewers:
      application_data = []
      for application in reviewer.reviews.all():  
          application_data.append(application)
      reviewer_list.append([reviewer.email, application_data])
    csv_data.append(reviewer_list)
    return csv_data


def export_reviewers_and_reviewees(request):
    time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="reviewers_{time}.csv"'
    writer = csv.writer(response)
    writer.writerow(["Reviewers and their applicants"])
    data = get_csv_data()
    for reviewer in data:
        writer.writerow([reviewer])
    return response
