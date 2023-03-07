# scripts/loaddb.py

import json
import csv
import random
import string
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import User


def get_model_data(model):
    questions = []
    with open('nov_29_12_41.json') as data:
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


def restore_users():
    data = get_model_data("accounts.user")
    for item in data:
        pk = item['pk']
        field_data = item['fields']
        field_data.pop('user_permissions')
        field_data.pop('groups')
        print(User.objects.create(
            pk=pk, **field_data))


def run():
    restore_users()