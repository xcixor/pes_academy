# scripts/restore.py

import json
import csv
import random
import string
from accounts.models import User
from application.models import *
from agripitch.models import *
from eligibility.models import *


def get_application_slugs_from_csv():
    applications_as__dict = []
    with open('lost.csv') as data_file:
        reader = csv.reader(data_file)
        for row in reader:
            slug = (row[0])
            head, sep, tail = slug.partition(' - ')
            applications_as__dict.append(
                {'slug': head, 'application_creator': row[1]})
    return applications_as__dict


def get_application_by_slug(model, slug):
    with open('data.json') as data:
        parsed_data = json.load(data)
        for item in parsed_data:
            if item['model'] == model and item['fields']['slug'] == slug:
                return item


def restore_applications():
    call_to_action = CallToAction.objects.first()
    application_data_from_csv = get_application_slugs_from_csv()
    for data_item in application_data_from_csv:
        item = get_application_by_slug(
            'application.application', data_item['slug'])
        field_data = item['fields']
        field_data.pop('application_creator')
        field_data.pop('call_to_action')
        user = User.objects.get(email=data_item['application_creator'])
        existing_application = None
        try:
            existing_application = Application.objects.get(pk=item['pk'])
        except Application.DoesNotExist as de:
            print(de)
        if not existing_application:
            application = Application.objects.create(
                pk=item['pk'], call_to_action=call_to_action,
                application_creator=user, **field_data)
            print(f'Created: {application.slug}')
        else:
            pk = item['pk']
        print(f'Application with pk: {pk} already exists')


def run():
    restore_applications()
