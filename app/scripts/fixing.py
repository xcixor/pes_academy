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

def get_model_data(model):
    questions = []
    with open('db_backups/nov_29_17_41.json') as data:
        parsed_data = json.load(data)
        for item in parsed_data:
            if item['model'] == model:
                questions.append(item)
    return questions


def restore_application_marks(owner_id):
    data = get_model_data("agripitch.applicationmarks")
    for item in data:
        field_data = item['fields']
        application_object = Application.objects.get(
            pk=field_data['application'])
        if str(application_object.application_creator) == owner_id:
            sub_criteria_item = SubCriteriaItem.objects.get(
                pk=field_data['question'])
            scoring = Scoring.objects.get(
                pk=field_data['scoring'])
            pk = item['pk']
            field_data.pop('application')
            field_data.pop('question')
            field_data.pop('scoring')
            try:
                print(ApplicationMarks.objects.update_or_create(
                    pk=pk, question=sub_criteria_item,
                    application=application_object,
                    scoring=scoring, **field_data))
            except:
                print("Marks already exist")

def restore_bonus(owner_id):
    data = get_model_data("eligibility.bonuspoints")
    for item in data:
        field_data = item['fields']
        application_object = Application.objects.get(
            pk=field_data['application'])
        if str(application_object.application_creator) == owner_id:
            pk = item['pk']
            step = ShortListGroup.objects.get(pk=field_data['step'])
            field_data.pop('application')
            field_data.pop('step')
            try:
                print(BonusPoints.objects.update_or_create(
                    pk=pk, application=application_object, step=step, **field_data))
            except:
                print("Bonus already exists")

def get_total_marks(owner_id):
    owner = User.objects.get(id=owner_id)
    app = Application.objects.get(application_creator=owner)
    return app.overall_score

def run():
    with open('esthers.csv') as data_file:
        reader = csv.reader(data_file)
        # for row in reader:
        #     owner_id = row[0]
        #     restore_bonus(owner_id)
        with open('esthers_marks_2.csv', 'w', newline='') as out_file:
            writer = csv.writer(out_file)
            for row in reader:
                owner_id = row[0]
                writer.writerow([owner_id, get_total_marks(owner_id)])
    print('done')
