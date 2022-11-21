# scripts/exports.py

import csv
from datetime import datetime
from agripitch.models import Application


def get_phase_csv_data(stage):
    csv_data = []
    applications = Application.objects.filter(stage=stage)
    for application in applications:
        csv_data.append([application.special_id, application.application_creator.email])
    return csv_data


def export_applications(stage, data):
    time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    file_name = f'csvs/{stage}_{time}'
    # no_of_columns = len(data[0])
    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        for item in data:
            # for column in no_of_columns:
            writer.writerow([item[0], item[1]])
    print('done')


def run():
    long_list_data = get_phase_csv_data('step_four')
    export_applications('Long List', long_list_data)
