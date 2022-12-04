# scripts/compile_evaluator_results.py
import csv
from accounts.models import User
from application.models import Application
from agripitch.models import SubCriteriaItem, ApplicationMarks


def can_convert_to_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def get_application(afdb_id):
    head, sep, tail = afdb_id.partition('-')
    user = None
    try:
        if can_convert_to_int(tail):
            user = User.objects.get(id=int(tail))
    except User.DoesNotExist:
        print('No user found for: ', afdb_id)
    application = None
    try:
        application = Application.objects.get(application_creator=user)
    except Application.DoesNotExist:
        print('No application found for: ', afdb_id)
    return application


def get_questions_from_headers(headers):
    questions = []
    for index, label in enumerate(headers):
        try:
            question = SubCriteriaItem.objects.get(label=label.strip())
            questions.append({'question': question, 'position': index})
        except SubCriteriaItem.DoesNotExist as de:
            print(de)
    return questions


def get_reviewer(email):
    try:
        user = User.objects.get(email=email)
        return user
    except User.DoesNotExist:
        print(f'Reviewer with email {email} not found')


def save_application_mark(data, reviewer, application, questions):
    for question in questions:
        if data['position'] == question['position']:
            print(question['question'], data['item'])
            sub_criteria_item = question['question']
            try:
                ApplicationMarks.objects.create(
                    question=sub_criteria_item,
                    application=application,
                    reviewer=reviewer,
                    score=data['item'],
                    scoring=sub_criteria_item.scoring.first())
            except Exception as e:
                print(e)


def compile(file):
    with open(file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        headers = rows.pop(0)
        questions = get_questions_from_headers(headers)
        rows.pop(0)
        # print(rows[0])
        for row in rows:
            application = get_application(row[3])
            reviewer = get_reviewer(row[33])
            for index, item in enumerate(row):
                row_data = {'item': item, 'position': index}
                # print(row_data)
                save_application_mark(
                    row_data, reviewer, application, questions)


def run():
    # file = input()
    compile('phase_2.csv')
    print('done')
