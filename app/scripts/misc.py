# scripts/misc.py
import csv
from agripitch.models import SubCriteriaItem, SubCriteriaItemResponse


def get_applications_by_language():
    sub_criteria = SubCriteriaItem.objects.get(label='Language *')
    all_by_language = SubCriteriaItemResponse.objects.filter(
        sub_criteria_item=sub_criteria, application__stage='step_five')
    english_speaking = [
        item.application for item in all_by_language if item.value == 'English']
    french_speaking = [
        item.application for item in all_by_language if item.value == 'French']
    print('All: ', len(all_by_language))
    print('English: ', len(english_speaking))
    print('French: ', len(french_speaking))


def export_google_supplementation_data():
    sub_criteria = SubCriteriaItem.objects.get(label='Entity Type *')
    all_by_entity = SubCriteriaItemResponse.objects.filter(
        sub_criteria_item=sub_criteria, application__stage='step_five')
    applications = [
        [
            str(item.application), item.value,
            sum(item.score for item in item.application.marks.all()),
            (sum(item.bonus for item in item.application.bonus.all()) + sum(item.score for item in item.application.marks.all()))] for item in all_by_entity]
    print(applications[0])
    with open('for_google_form.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "ID", "Entity type",
                "Total Marks [Eligibility + Document Verification]",
                "Total Marks [Eligibility + Document Verification + Bonus]"])
        for application in applications:
            writer.writerow(
                [application[0], application[1],
                 application[2], application[3], ])


def run():
    export_google_supplementation_data()
