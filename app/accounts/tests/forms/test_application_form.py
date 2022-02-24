from django.test import RequestFactory
from django.test.client import Client
from accounts.tests.common import AccountsBaseTestCase
from application.forms import ApplicationForm
from application.models import Milestone


class ApplicationFormTestCase(AccountsBaseTestCase):

    def setUp(self) -> None:
        super(ApplicationFormTestCase, self).setUp()
        mileston_one = self.create_milestone()
        mileston_two = self.create_another_milestone()
        self.form_data = {
            'email': 'test@gmail.com',
            'full_name': 'Test Name',
            'age': 'range_one',
            'gender': 'male',
            'preferred_language': 'french',
            'organization_name': 'Big Tech',
            'facebook_link': 'https://www.facebook.com/bigtech',
            'value_chain': 'chain_three',
            'existence_period': 'period_two',
            'stage': 'stage_one',
            'impact': 'We beat it',
            'milestones': [mileston_one.id, mileston_two.id]
        }
        self.client = Client()
        self.factory = RequestFactory()
        self.request = self.factory.get("/")
        self.form = ApplicationForm(self.request, self.form_data)

    def test_validates_form(self):
        self.assertTrue(self.form.is_valid())

    def test_cleans_milestones(self):
        Milestone.objects.create(milestone='Another milestone')
        Milestone.objects.create(milestone='Yet another milestone')
        milestones = [milestone.id for milestone in Milestone.objects.all()]
        self.form_data['milestones'] = milestones
        form = ApplicationForm(self.request, self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['milestones'][0],
            'You cannot select more than 3 items.')

    def test_saves_user(self):
        self.assertTrue(self.form.is_valid())
        self.assertTrue(self.user)

    def test_saves_business(self):
        is_valid = self.form.is_valid()
        self.assertTrue(is_valid)
        business = self.form.save_business(self.user)
        self.assertTrue(business)

    def test_updates_business_if_already_exists(self):
        self.assertTrue(self.form.is_valid())
        business, created = self.form.save_business(self.user)
        self.assertEqual(business.organization_owner, self.user)
        self.assertTrue(created)
        self.form_data['facebook_link'] = 'https://www.facebook.com/smalltech'
        self.form_data['twitter_link'] = 'https://www.twitter.com/bigtech'
        business, created = self.form.save_business(self.user)
        self.assertEqual(business.organization_owner, self.user)
        self.assertFalse(created)
        self.assertTrue(business.twitter_link)

    def test_cannot_save_business_if_data_invalid(self):
        self.assertTrue(self.form.is_valid())
        self.form_data['facebook_link'] = 'https//www.facebook/smalltech'
        form = ApplicationForm(self.form_data)
        business = form.save_business(self.user)
        self.assertFalse(business)

    def test_saves_milestone(self):
        self.assertTrue(self.form.is_valid())
        business = self.form.save_business(self.user)[0]
        response = self.form.save_milestone(business)
        self.assertTrue(response)
        [self.assertEqual(milestone.businesses.first(), business)
            for milestone in Milestone.objects.all()]

    def test_adds_milestones_choices_from_db(self):
        ids_in_db = [(milestone.id, milestone.milestone)
                     for milestone in Milestone.objects.all()]
        self.assertEqual(self.form.fields['milestones'].choices, ids_in_db)

    def test_saves_covid_impact_on_business(self):
        self.assertTrue(self.form.is_valid())
        business = self.form.save_business(self.user)[0]
        impact = self.form.save_covid_impact(business)
        self.assertTrue(impact)

    def test_updates_covid_impact_on_business_if_same_business(self):
        self.assertTrue(self.form.is_valid())
        business = self.form.save_business(self.user)[0]
        impact, created = self.form.save_covid_impact(business)
        self.assertEqual(impact.impact, 'We beat it')
        self.assertTrue(created)
        self.form_data['impact'] = 'We lost Revenue'
        form = ApplicationForm(self.request, self.form_data)
        impact, created = form.save_covid_impact(business)
        self.assertFalse(created)
        self.assertEqual(impact.impact, 'We lost Revenue')
