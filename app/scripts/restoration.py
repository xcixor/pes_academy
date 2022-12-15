# scripts/misc.py
import csv
from django_countries import countries as dj_countries
from agripitch.models import SubCriteriaItem, SubCriteriaItemResponse, Application, ApplicationMarks
from accounts.models import User
from application.models import ApplicationReview
from eligibility.models import BonusPoints


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


def get_application(owner_id):
    owner = User.objects.get(id=owner_id)
    app = Application.objects.get(application_creator=owner)
    return app


def get_country_response_fo_application(application):
    sub_criteria = SubCriteriaItem.objects.get(label='Country *')
    try:
        response = SubCriteriaItemResponse.objects.get(
            application=application, sub_criteria_item=sub_criteria)
        return dict(dj_countries)[response.value]
    except SubCriteriaItemResponse.DoesNotExist:
        print(f'Country for {application} not found')


def get_subcriteria_response_for_application(subcriteria, application):
    sub_criteria = SubCriteriaItem.objects.get(label=subcriteria)
    try:
        response = SubCriteriaItemResponse.objects.get(
            application=application, sub_criteria_item=sub_criteria)
        return response.value
    except SubCriteriaItemResponse.DoesNotExist:
        print(f'Country for {application} not found')


def export_shortlist_metric():
    with open('shortlist.csv', 'r') as file:
        reader = csv.reader(file)
        with open('company_names.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for row in reader:
                owner_id = row[0]
                writer.writerow([f'AfDB-{owner_id}', get_subcriteria_response_for_application(
                    'Company Name *', get_application(owner_id))])


def export_google_supplementation_data():
    sub_criteria = SubCriteriaItem.objects.get(label='Entity Type *')
    all_by_entity = SubCriteriaItemResponse.objects.filter(
        sub_criteria_item=sub_criteria, application__stage='step_five')
    applications = [
        [
            str(item.application.application_creator), item.value, get_country(
                item.application),
            sum(item.score for item in item.application.marks.all()),
            (sum(item.bonus for item in item.application.bonus.all()) + sum(item.score for item in item.application.marks.all()))] for item in all_by_entity]
    sorted_queryset = sorted(
        applications, key=lambda t: t[4], reverse=True)
    with open('for_google_form.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "ID", "Entity type", "Country",
                "Total Marks [Eligibility + Document Verification]",
                "Total Marks [Eligibility + Document Verification + Bonus]"])
        for application in sorted_queryset:
            writer.writerow(
                [application[0], application[1],
                 application[2], application[3], application[4]])


def generate_reviewer_review_list(email):
    reviewer = User.objects.get(email=email)
    with open(f"csvs/{reviewer.email}.csv", 'w') as file:
        writer = csv.writer(file)
        writer.writerow([reviewer.email])
        for review in reviewer.reviews.all():
            writer.writerow([review.application])
    print('done')


def show_diana_extra():
    the_38 = []
    with open('shortlist.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            owner_id = row[0]
            the_38.append(get_application(owner_id).id)
    diana = User.objects.get(email='gichaga@privateequity-support.com')
    print(diana.reviews.count())
    for review in diana.reviews.all():
        if review.application.id not in the_38:
            print(review.application.application_creator.special_id)


def show_reviewers(owner_id):
    owner = User.objects.get(id=owner_id)
    app = Application.objects.get(application_creator=owner)
    for review in app.reviewers.all():
        print(review.reviewer.email)
    # ema = User.objects.get(email='emmanuel@privateequity-support.com')
    # print(ApplicationReview.objects.create(application=app, reviewer=ema))


def check_marks(owner_id):
    owner = User.objects.get(id=owner_id)
    app = Application.objects.get(application_creator=owner)
    marks = ApplicationMarks.objects.filter(application=app)
    print(marks)
    marks = sum(item.score for item in marks)
    bonus = BonusPoints.objects.filter(application=app)
    total_bonus = sum(item.bonus for item in bonus)
    print(marks+total_bonus)


def assign_shortlist(application):
    reviewers = []
    angie = User.objects.get(email='amkariuki@gmail.com')
    kahasha = User.objects.get(email='G.KAHASHA@AFDB.ORG')
    aida = User.objects.get(email='a.bakayoko@afdb.org')
    wilfred = User.objects.get(email='wilfred.mworia@pfan.net')
    diana = User.objects.get(email='gichaga@privateequity-support.com')
    pta = User.objects.get(email='peter@privateequity-support.com')
    edson = User.objects.get(email='E.MPYISI@afdb.org')
    reviewers.append(edson)
    reviewers.append(wilfred)
    reviewers.append(pta)
    reviewers.append(kahasha)
    reviewers.append(aida)
    reviewers.append(diana)
    reviewers.append(angie)
    for reviewer in reviewers:
        print(ApplicationReview.objects.create(
            reviewer=reviewer, application=application))


def show_application_reviews():
    reviewers = []
    # angie = User.objects.get(email='amkariuki@gmail.com')
    # kahasha = User.objects.get(email='G.KAHASHA@AFDB.ORG')
    # aida = User.objects.get(email='a.bakayoko@afdb.org')
    # wilfred = User.objects.get(email='wilfred.mworia@pfan.net')
    # edson = User.objects.get(email='E.MPYISI@afdb.org')
    diana = User.objects.get(email='gichaga@privateequity-support.com')
    reviewers.append(diana)
    # reviewers.append(wilfred)
    # reviewers.append(kahasha)
    # reviewers.append(aida)
    for reviewer in reviewers:
        print(reviewer.reviews.count(), reviewer.email)


def run():
    # export_google_supplementation_data()
    # email = input()
    # generate_reviewer_review_list(email)
    # user_id = input()
    # show_reviewers(user_id)
    # owner_id = input()
    # check_marks(owner_id)
    # show_reviewers(owner_id)
    # remove_application_reviews()
    with open('extra_3.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            owner_id = row[0]
            try:
                owner = User.objects.get(id=owner_id)
                application = Application.objects.get(
                    application_creator=owner)
                assign_shortlist(application)
            except:
                print(f'{owner_id} erred')
    show_application_reviews()
    # export_shortlist_metric()
    # show_diana_extra()
    print('done')
