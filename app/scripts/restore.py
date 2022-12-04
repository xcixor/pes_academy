# scripts/restore.py

import json
import csv
import random
import string
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
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
    with open('dump.json') as data:
        parsed_data = json.load(data)
        for item in parsed_data:
            if item['model'] == model and item['fields']['slug'] == slug:
                return item


def get_model_data(model):
    questions = []
<<<<<<< HEAD
<<<<<<< HEAD
    with open('nov_29_17_41.json') as data:
=======
    with open('nov_29_12_41.json') as data:
>>>>>>> 4ab385c (chore(scripts): update scripts)
=======
    with open('nov_29_12_41.json') as data:
<<<<<<< HEAD
>>>>>>> 4ab385c8 (chore(scripts): update scripts)
=======
>>>>>>> 4ab385c (chore(scripts): update scripts)
>>>>>>> 9ef1a1e7 (chore(scripts): update scripts)
        parsed_data = json.load(data)
        for item in parsed_data:
            if item['model'] == model:
                questions.append(item)
    return questions


def create_user(email):
    password = ''.join(random.choices(
        string.ascii_uppercase + string.ascii_lowercase, k=10))
    user = User.objects._create_user(email, password, email=email)
    return user


def restore_call_to_action():
    data = get_model_data("application.calltoaction")
    for item in data:
        pk = item['pk']
        field_data = item['fields']
        print(CallToAction.objects.create(
            pk=pk, **field_data))


def restore_applications():
    call_to_action = CallToAction.objects.first()
    data = get_model_data("application.application")
    for item in data:
        field_data = item['fields']
        user = User.objects.get(pk=field_data['application_creator'])
        field_data.pop('application_creator')
        field_data.pop('call_to_action')
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


def restore_shortlist():
    call_to_action = CallToAction.objects.first()
    data = get_model_data("agripitch.shortlist")
    for item in data:
        print(item)
        pk = item['pk']
        field_data = item['fields']
        field_data.pop('competition')
<<<<<<< HEAD
<<<<<<< HEAD
        try:
            print(ShortList.objects.create(
                pk=pk, competition=call_to_action, **field_data))
        except:
            print("Shorty might already exist")
=======
        print(ShortList.objects.create(
            pk=pk, competition=call_to_action, **field_data))
>>>>>>> 4ab385c (chore(scripts): update scripts)
=======
        print(ShortList.objects.create(
            pk=pk, competition=call_to_action, **field_data))
<<<<<<< HEAD
>>>>>>> 4ab385c8 (chore(scripts): update scripts)
=======
>>>>>>> 4ab385c (chore(scripts): update scripts)
>>>>>>> 9ef1a1e7 (chore(scripts): update scripts)


def restore_users():
    data = get_model_data("accounts.user")
    for item in data:
        pk = item['pk']
        field_data = item['fields']
        field_data.pop('user_permissions')
        if field_data['groups']:
            field_data.pop('groups')
            user = User.objects.create(
                pk=pk, **field_data)

            reviewers_group, created = Group.objects.get_or_create(
                name='reviewers')
            content_type = ContentType.objects.get_for_model(Application)
            permission, created = Permission.objects.get_or_create(
                codename='can_view_application',
                name='Can view application',
                content_type=content_type)
            reviewers_group.permissions.add(permission)
            user.groups.add(reviewers_group)
            print(user)
        else:
            field_data.pop('groups')
            print(User.objects.create(
                pk=pk, **field_data))


def restore_criteriaitems():
    shortlist = ShortList.objects.first()
    data = get_model_data("agripitch.criteriaitem")
    for item in data:
        print(item)
        pk = item['pk']
        field_data = item['fields']
        field_data.pop('shortlist')
<<<<<<< HEAD
<<<<<<< HEAD
        try:
            print(CriteriaItem.objects.create(
                pk=pk, shortlist=shortlist, **field_data))
        except:
            print('Criteria item exists')
=======
        print(CriteriaItem.objects.create(
            pk=pk, shortlist=shortlist, **field_data))
>>>>>>> 4ab385c (chore(scripts): update scripts)
=======
        print(CriteriaItem.objects.create(
            pk=pk, shortlist=shortlist, **field_data))
<<<<<<< HEAD
>>>>>>> 4ab385c8 (chore(scripts): update scripts)
=======
>>>>>>> 4ab385c (chore(scripts): update scripts)
>>>>>>> 9ef1a1e7 (chore(scripts): update scripts)


def restore_questions():
    data = get_model_data("agripitch.subcriteriaitem")
    for item in data:
        field_data = item['fields']
        criteria = CriteriaItem.objects.get(pk=field_data['criteria'])
        pk = item['pk']
        field_data.pop('criteria')
<<<<<<< HEAD
<<<<<<< HEAD
        try:
            print(SubCriteriaItem.objects.create(
                pk=pk, criteria=criteria, **field_data))
        except:
            print("Question might already exist")
=======
        print(SubCriteriaItem.objects.create(
            pk=pk, criteria=criteria, **field_data))
>>>>>>> 4ab385c (chore(scripts): update scripts)
=======
        print(SubCriteriaItem.objects.create(
            pk=pk, criteria=criteria, **field_data))
<<<<<<< HEAD
>>>>>>> 4ab385c8 (chore(scripts): update scripts)
=======
>>>>>>> 4ab385c (chore(scripts): update scripts)
>>>>>>> 9ef1a1e7 (chore(scripts): update scripts)


def restore_questions_choices():
    data = get_model_data("agripitch.subcriteriaitemchoice")
    for item in data:
        field_data = item['fields']
        sub_criteria_item = SubCriteriaItem.objects.get(
            pk=field_data['sub_criteria_item'])
        pk = item['pk']
        field_data.pop('sub_criteria_item')
<<<<<<< HEAD
<<<<<<< HEAD
        try:
            print(SubCriteriaItemChoice.objects.create(
                pk=pk, sub_criteria_item=sub_criteria_item, **field_data))
        except:
            print("Choice might already exist")
=======
        print(SubCriteriaItemChoice.objects.create(
            pk=pk, sub_criteria_item=sub_criteria_item, **field_data))
>>>>>>> 4ab385c (chore(scripts): update scripts)
=======
        print(SubCriteriaItemChoice.objects.create(
            pk=pk, sub_criteria_item=sub_criteria_item, **field_data))
<<<<<<< HEAD
>>>>>>> 4ab385c8 (chore(scripts): update scripts)
=======
>>>>>>> 4ab385c (chore(scripts): update scripts)
>>>>>>> 9ef1a1e7 (chore(scripts): update scripts)


def clean_list_value(value):
    value_list = []
    if value:
        for item in value:
            without_commas = item.replace('", "', '')
            without_commas = without_commas.replace('"', '')
            without_braces = without_commas.replace('[', '')
            without_braces = without_braces.replace(']', '')
            value_list.append(without_braces)
    return value_list


def restore_textual_responses():
<<<<<<< HEAD
<<<<<<< HEAD
    data = get_model_data("agripitch.subcriteriaitemresponse")
    for item in data:
        field_data = item['fields']
        application_object = Application.objects.get(
            pk=field_data['application'])
        if application_object.pk == field_data['application']:
            sub_criteria_item = SubCriteriaItem.objects.get(
                pk=field_data['sub_criteria_item'])
            pk = item['pk']
            field_data.pop('application')
            field_data.pop('sub_criteria_item')
            if sub_criteria_item.type == 'multiplechoicefield':
                list_value = clean_list_value(
                    json.loads(field_data['list_value']))
                field_data.pop('list_value')
                try:
=======
=======
<<<<<<< HEAD
>>>>>>> 4ab385c8 (chore(scripts): update scripts)
=======
>>>>>>> 4ab385c (chore(scripts): update scripts)
>>>>>>> 9ef1a1e7 (chore(scripts): update scripts)
    application_data_from_csv = get_application_slugs_from_csv()
    for application in application_data_from_csv:
        application_object = Application.objects.get(slug=application['slug'])
        data = get_model_data("agripitch.subcriteriaitemresponse")
        for item in data:
            field_data = item['fields']
            if application_object.pk == field_data['application']:
                sub_criteria_item = SubCriteriaItem.objects.get(
                    pk=field_data['sub_criteria_item'])
                pk = item['pk']
                field_data.pop('application')
                field_data.pop('sub_criteria_item')
                if sub_criteria_item.type == 'multiplechoicefield':
                    list_value = clean_list_value(
                        json.loads(field_data['list_value']))
                    field_data.pop('list_value')
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 4ab385c (chore(scripts): update scripts)
=======
>>>>>>> 9ef1a1e7 (chore(scripts): update scripts)
>>>>>>> 4ab385c (chore(scripts): update scripts)
=======
>>>>>>> 4ab385c8 (chore(scripts): update scripts)
                    print(SubCriteriaItemResponse.objects.create(
                        pk=pk,
                        sub_criteria_item=sub_criteria_item,
                        application=application_object,
                        list_value=list_value,
                        **field_data))
<<<<<<< HEAD
<<<<<<< HEAD
                except:
                    print("response already exist")
            else:
                try:
                    print(SubCriteriaItemResponse.objects.create(
                        pk=pk, sub_criteria_item=sub_criteria_item,
                        application=application_object, **field_data))
                except:
                    print("response already exist")


def restore_document_responses():
    data = get_model_data("agripitch.subcriteriaitemdocumentresponse")
    for item in data:
        field_data = item['fields']
        application_object = Application.objects.get(
            pk=field_data['application'])
        sub_criteria_item = SubCriteriaItem.objects.get(
            pk=field_data['sub_criteria_item'])
        pk = item['pk']
        field_data.pop('application')
        field_data.pop('sub_criteria_item')
        if sub_criteria_item.type == 'file':
            try:
                print(SubCriteriaItemDocumentResponse.objects.create(
                    pk=pk, sub_criteria_item=sub_criteria_item,
                    application=application_object, **field_data))
            except:
                print("File already exists")
=======
=======
<<<<<<< HEAD
>>>>>>> 4ab385c8 (chore(scripts): update scripts)
=======
>>>>>>> 4ab385c (chore(scripts): update scripts)
>>>>>>> 9ef1a1e7 (chore(scripts): update scripts)
                else:
                    print(SubCriteriaItemResponse.objects.create(
                        pk=pk, sub_criteria_item=sub_criteria_item,
                        application=application_object, **field_data))


def restore_document_responses():
    application_data_from_csv = get_application_slugs_from_csv()
    for application in application_data_from_csv:
        application_object = Application.objects.get(slug=application['slug'])
        data = get_model_data("agripitch.subcriteriaitemdocumentresponse")
        for item in data:
            field_data = item['fields']
            if application_object.pk == field_data['application']:
                sub_criteria_item = SubCriteriaItem.objects.get(
                    pk=field_data['sub_criteria_item'])
                pk = item['pk']
                field_data.pop('application')
                field_data.pop('sub_criteria_item')
                if sub_criteria_item.type == 'file':
                    print(SubCriteriaItemDocumentResponse.objects.create(
                        pk=pk, sub_criteria_item=sub_criteria_item,
                        application=application_object, **field_data))
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 4ab385c (chore(scripts): update scripts)
=======
>>>>>>> 9ef1a1e7 (chore(scripts): update scripts)
>>>>>>> 4ab385c (chore(scripts): update scripts)
=======
>>>>>>> 4ab385c8 (chore(scripts): update scripts)


def restore_scales():
    data = get_model_data("agripitch.scale")
    for item in data:
        field_data = item['fields']
        pk = item['pk']
<<<<<<< HEAD
<<<<<<< HEAD
        try:
            print(Scale.objects.create(
                pk=pk, **field_data))
        except:
            print("Scale already exists")
=======
        print(Scale.objects.create(
            pk=pk, **field_data))
>>>>>>> 4ab385c (chore(scripts): update scripts)
=======
        print(Scale.objects.create(
            pk=pk, **field_data))
<<<<<<< HEAD
>>>>>>> 4ab385c8 (chore(scripts): update scripts)
=======
>>>>>>> 4ab385c (chore(scripts): update scripts)
>>>>>>> 9ef1a1e7 (chore(scripts): update scripts)


def restore_scale_items():
    data = get_model_data("agripitch.scaleitem")
    for item in data:
        field_data = item['fields']
        pk = item['pk']
<<<<<<< HEAD
<<<<<<< HEAD
        try:
            print(ScaleItem.objects.create(
                pk=pk, **field_data))
        except:
            print("Scale Item already exists")
=======
        print(ScaleItem.objects.create(
            pk=pk, **field_data))
>>>>>>> 4ab385c (chore(scripts): update scripts)
=======
        print(ScaleItem.objects.create(
            pk=pk, **field_data))
<<<<<<< HEAD
>>>>>>> 4ab385c8 (chore(scripts): update scripts)
=======
>>>>>>> 4ab385c (chore(scripts): update scripts)
>>>>>>> 9ef1a1e7 (chore(scripts): update scripts)


def restore_scoring_items():
    data = get_model_data("agripitch.scoringitems")
    for item in data:
        field_data = item['fields']
        pk = item['pk']
        scale = Scale.objects.get(pk=field_data['scale'])
        item = ScaleItem.objects.get(pk=field_data['item'])
<<<<<<< HEAD
<<<<<<< HEAD
        try:
            print(ScoringItems.objects.create(
                pk=pk, scale=scale, item=item))
        except:
            print("Scoring item exists")
=======
        print(ScoringItems.objects.create(
            pk=pk, scale=scale, item=item))
>>>>>>> 4ab385c (chore(scripts): update scripts)
=======
        print(ScoringItems.objects.create(
            pk=pk, scale=scale, item=item))
<<<<<<< HEAD
>>>>>>> 4ab385c8 (chore(scripts): update scripts)
=======
>>>>>>> 4ab385c (chore(scripts): update scripts)
>>>>>>> 9ef1a1e7 (chore(scripts): update scripts)


def restore_scoring():
    data = get_model_data("agripitch.scoring")
    for item in data:
        field_data = item['fields']
        pk = item['pk']
        scale = Scale.objects.get(pk=field_data['scale'])
        question = SubCriteriaItem.objects.get(
            pk=field_data['question'])
<<<<<<< HEAD
<<<<<<< HEAD
        field_data.pop('question')
        field_data.pop('scale')
        try:
            print(Scoring.objects.create(
                pk=pk, scale=scale, question=question, **field_data))
        except:
            print('Scoring exists')


def restore_application_marks():
    data = get_model_data("agripitch.applicationmarks")
    for item in data:
        field_data = item['fields']
        application_object = Application.objects.get(
            pk=field_data['application'])
        sub_criteria_item = SubCriteriaItem.objects.get(
            pk=field_data['question'])
        scoring = Scoring.objects.get(
            pk=field_data['scoring'])
        pk = item['pk']
        field_data.pop('application')
        field_data.pop('question')
        field_data.pop('scoring')
        try:
            print(ApplicationMarks.objects.create(
                pk=pk, question=sub_criteria_item,
                application=application_object,
                scoring=scoring, **field_data))
        except:
            print("Marks already exist")


def restore_application_documents():
    data = get_model_data("application.applicationdocument")
    for item in data:
        field_data = item['fields']
        application_object = Application.objects.get(
            pk=field_data['application'])
        pk = item['pk']
        field_data.pop('application')
        try:
            print(ApplicationDocument.objects.create(
                pk=pk, application=application_object, **field_data))
        except:
            print("Document exists")


def restore_application_prompt():
    data = get_model_data("application.applicationprompt")
    for item in data:
        field_data = item['fields']
        application_object = Application.objects.get(
            pk=field_data['application'])
        pk = item['pk']
        field_data.pop('application')
        prompt = SubCriteriaItem.objects.get(
            pk=field_data['prompt'])
        field_data.pop('prompt')
        reviewer = User.objects.get(
            pk=field_data['reviewer'])
        field_data.pop('reviewer')
        print(ApplicationPrompt.objects.create(
            pk=pk, application=application_object,
            prompt=prompt,
            reviewer=reviewer, **field_data))


def restore_application_comment():
    data = get_model_data("application.applicationcomment")
    for item in data:
        field_data = item['fields']
        application_object = Application.objects.get(
            pk=field_data['application'])
        pk = item['pk']
        field_data.pop('application')
        reviewer = User.objects.get(
            pk=field_data['reviewer'])
        field_data.pop('reviewer')
        try:
            print(ApplicationComment.objects.create(
                pk=pk, application=application_object,
                reviewer=reviewer, **field_data))
        except:
            print('Comment already exists')
=======
=======
<<<<<<< HEAD
>>>>>>> 4ab385c8 (chore(scripts): update scripts)
=======
>>>>>>> 4ab385c (chore(scripts): update scripts)
>>>>>>> 9ef1a1e7 (chore(scripts): update scripts)
        print(Scoring.objects.create(
            pk=pk, scale=scale, question=question, **field_data))


def restore_application_marks():
    application_data_from_csv = get_application_slugs_from_csv()
    for application in application_data_from_csv:
        application_object = Application.objects.get(slug=application['slug'])
        data = get_model_data("agripitch.applicationmarks")
        for item in data:
            field_data = item['fields']
            if application_object.pk == field_data['application']:
                sub_criteria_item = SubCriteriaItem.objects.get(
                    pk=field_data['question'])
                scoring = Scoring.objects.get(
                    pk=field_data['scoring'])
                pk = item['pk']
                field_data.pop('application')
                field_data.pop('question')
                field_data.pop('scoring')
                print(ApplicationMarks.objects.create(
                    pk=pk, question=sub_criteria_item,
                    application=application_object,
                    scoring=scoring, **field_data))


def restore_application_documents():
    application_data_from_csv = get_application_slugs_from_csv()
    for application in application_data_from_csv:
        application_object = Application.objects.get(slug=application['slug'])
        data = get_model_data("application.applicationdocument")
        for item in data:
            field_data = item['fields']
            if application_object.pk == field_data['application']:
                pk = item['pk']
                field_data.pop('application')
                print(ApplicationDocument.objects.create(
                    pk=pk, application=application_object, **field_data))


def restore_application_prompt():
    application_data_from_csv = get_application_slugs_from_csv()
    for application in application_data_from_csv:
        application_object = Application.objects.get(slug=application['slug'])
        data = get_model_data("application.applicationdocument")
        for item in data:
            field_data = item['fields']
            if application_object.pk == field_data['application']:
                pk = item['pk']
                field_data.pop('application')
                prompt = SubCriteriaItem.objects.get(
                    pk=field_data['prompt'])
                field_data.pop('prompt')
                reviewer = User.objects.get(
                    pk=field_data['reviewer'])
                field_data.pop('prompt')
                field_data.pop('reviewer')
                print(ApplicationPrompt.objects.create(
                    pk=pk, application=application_object,
                    prompt=prompt,
                    reviewer=reviewer, **field_data))


def restore_application_comment():
    application_data_from_csv = get_application_slugs_from_csv()
    for application in application_data_from_csv:
        application_object = Application.objects.get(slug=application['slug'])
        data = get_model_data("application.applicationcomment")
        for item in data:
            field_data = item['fields']
            if application_object.pk == field_data['application']:
                pk = item['pk']
                field_data.pop('application')
                reviewer = User.objects.get(
                    pk=field_data['reviewer'])
                field_data.pop('prompt')
                field_data.pop('reviewer')
                try:
                    print(ApplicationComment.objects.create(
                        pk=pk, application=application_object,
                        reviewer=reviewer, **field_data))
                except:
                    print('Comment already exists')
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 4ab385c (chore(scripts): update scripts)
=======
>>>>>>> 9ef1a1e7 (chore(scripts): update scripts)
>>>>>>> 4ab385c (chore(scripts): update scripts)
=======
>>>>>>> 4ab385c8 (chore(scripts): update scripts)


def restore_shortlistgroup():
    data = get_model_data("eligibility.shortlistgroup")
    for item in data:
        field_data = item['fields']
        pk = item['pk']
<<<<<<< HEAD
<<<<<<< HEAD
        try:
            print(ShortListGroup.objects.create(
                pk=pk, **field_data))
        except:
            print('Group already exists')
=======
        print(ShortListGroup.objects.create(
            pk=pk, **field_data))
>>>>>>> 4ab385c (chore(scripts): update scripts)
=======
        print(ShortListGroup.objects.create(
            pk=pk, **field_data))
<<<<<<< HEAD
>>>>>>> 4ab385c8 (chore(scripts): update scripts)
=======
>>>>>>> 4ab385c (chore(scripts): update scripts)
>>>>>>> 9ef1a1e7 (chore(scripts): update scripts)


def restore_shortlistgroupitem():
    data = get_model_data("eligibility.shortlistgroupitems")
    for item in data:
        field_data = item['fields']
        pk = item['pk']
        group = ShortListGroup.objects.get(pk=field_data['group'])
        question = SubCriteriaItem.objects.get(
            pk=field_data['question'])
<<<<<<< HEAD
<<<<<<< HEAD
        try:
            print(ShortListGroupItems.objects.create(
                pk=pk, group=group, question=question))
        except:
            print("Group Item already exists")


def restore_bonus():
    data = get_model_data("eligibility.bonuspoints")
    for item in data:
        field_data = item['fields']
        application_object = Application.objects.get(
            pk=field_data['application'])
        pk = item['pk']
        step = ShortListGroup.objects.get(pk=field_data['step'])
        field_data.pop('application')
        field_data.pop('step')
        try:
            print(BonusPoints.objects.create(
                pk=pk, application=application_object, step=step, **field_data))
        except:
            print("Bonus already exists")


def restore_reviews():
    data = get_model_data("application.applicationreview")
    for item in data:
        field_data = item['fields']
        pk = item['pk']
        application = Application.objects.get(pk=field_data['application'])
        reviewer = User.objects.get(
            pk=field_data['reviewer'])
        field_data.pop('application')
        field_data.pop('reviewer')
        try:
            print(ApplicationReview.objects.create(
                pk=pk, application=application, reviewer=reviewer, **field_data))
        except:
            print('Review exists')
=======
=======
<<<<<<< HEAD
>>>>>>> 4ab385c8 (chore(scripts): update scripts)
=======
>>>>>>> 4ab385c (chore(scripts): update scripts)
>>>>>>> 9ef1a1e7 (chore(scripts): update scripts)
        print(ShortListGroupItems.objects.create(
            pk=pk, group=group, question=question))


def restore_bonus():
    application_data_from_csv = get_application_slugs_from_csv()
    for application in application_data_from_csv:
        application_object = Application.objects.get(slug=application['slug'])
        data = get_model_data("eligibility.bonuspoints")
        for item in data:
            field_data = item['fields']
            if application_object.pk == field_data['application']:
                pk = item['pk']
                step = ShortListGroup.objects.get(pk=field_data['step'])
                field_data.pop('application')
                field_data.pop('step')
                print(BonusPoints.objects.create(
                    pk=pk, application=application_object,
                    step=step, **field_data))
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 4ab385c (chore(scripts): update scripts)
=======
>>>>>>> 9ef1a1e7 (chore(scripts): update scripts)
>>>>>>> 4ab385c (chore(scripts): update scripts)
=======
>>>>>>> 4ab385c8 (chore(scripts): update scripts)


def run():
    # restore_users()
    # restore_call_to_action()
<<<<<<< HEAD
<<<<<<< HEAD
    # restore_applications()

    # restore_shortlist()
    # restore_criteriaitems()
    # restore_questions()
    # restore_questions_choices()
    # restore_textual_responses()

    # restore_scales()
    # restore_scale_items()
    # restore_scoring_items()
    # restore_scoring()
    # restore_application_marks()

    # restore_application_comment()
    # restore_application_prompt()

    # restore_shortlistgroup()
    # restore_shortlistgroupitem()
    # restore_bonus()

    # restore_document_responses()
    # restore_application_documents()
    # restore_reviews()
<<<<<<< HEAD
    pass
=======
    restore_applications()
>>>>>>> 4ab385c (chore(scripts): update scripts)
=======
    restore_applications()
<<<<<<< HEAD
>>>>>>> 4ab385c8 (chore(scripts): update scripts)
=======
>>>>>>> 4ab385c (chore(scripts): update scripts)
<<<<<<< HEAD
>>>>>>> 9ef1a1e7 (chore(scripts): update scripts)
=======
=======
    print('done')
>>>>>>> e2bf5cc (chore(scripts): add a script to read Phase 2 Googel doc responses and save to db)
>>>>>>> 2af7fa2a (chore(scripts): add a script to read Phase 2 Googel doc responses and save to db)
