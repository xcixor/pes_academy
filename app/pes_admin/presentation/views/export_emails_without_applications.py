import csv
from django.http import HttpResponse
from django.utils import timezone
from accounts.models import User
from application.models import Application


def emails():
    users_with_applications_emails = Application.objects.all().values_list(
        'application_creator__email', flat=True)
    all_users_emails = User.objects.all().values_list(
        'email', flat=True)
    difference_in_emails = [
        item for item in all_users_emails if item
        not in users_with_applications_emails]
    return difference_in_emails


def export_emails_without_applications(request):
    filename = f'emails_{timezone.now()}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow(["Emails that haven't started the application process"])
    data = emails()
    for item in data:
        writer.writerow([item])
    return response
