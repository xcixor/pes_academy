from django.contrib.auth import get_user_model
from application.tests.common import ApplicationBaseTestCase
from application.models import BusinessOrganization, Milestone, CovidImpact


User = get_user_model()


class AccountsBaseTestCase(ApplicationBaseTestCase):

    def setUp(self):
        super(AccountsBaseTestCase, self).setUp()

    def create_user(self):
        user = User.objects.create(
            email='test@gmail.com',
            age=26,
            gender='male',
            preferred_language='Portuguese',
            full_name='Jim jones'
        )
        return user

    def create_business(self):
        link = BusinessOrganization.objects.create(
            organization_owner=self.create_user(),
            organization_name='Caravan Tech',
            facebook_link='https://faceme.com',
            twitter_link='https://twitterme.com',
            whatsapp_business_link='https://whatsapp.com',
            instagram_link='https://instagram.com',
            value_chain='chain_one',
            existence_period='period_one',
            stage='stage_one',
        )
        return link

    def create_milestone(self):
        milestone = Milestone.objects.create(
            milestone='Revenue Growth'
        )
        return milestone

    def create_another_milestone(self):
        milestone = Milestone.objects.create(
            milestone='Market Segmentation'
        )
        return milestone

    def create_covid_impact(self):
        impact = CovidImpact.objects.create(
            business=self.create_business(),
            impact='Loss of Customers',
        )
        return impact
