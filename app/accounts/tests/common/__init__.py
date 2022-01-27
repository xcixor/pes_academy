from django.contrib.auth import get_user_model
from sme.tests.common import SMETestCase
# from accounts.models import BusinessOrganization, Milestone, CovidImpact


User = get_user_model()


class AccountsBaseTestCase(SMETestCase):

    def setUp(self):
        super(AccountsBaseTestCase, self).setUp()

    def create_user(self):
        user = User.objects.create(
            email_address='test@gmail.com',
            native_language='Portuguese',
            age=26,
            gender='male',
            preferred_email_address='test@gmail.com',
            preferred_language='Portuguese',
            full_name='Jim jones'
        )
        return user

    def create_business(self):
        link = BusinessOrganization.objects.create(
            owner=self.create_user(),
            name='Caravan Tech',
            facebook_link='https://faceme.com',
            twitter_link='https://twitterme.com',
            whatsapp_business='https://whatsapp.com',
            instagram_link='https://instagram.com',
            value_chain='chain_one',
            existence_period='period_one',
            stage='stage_one',
        )
        return link

    def create_milestone(self):
        milestone = Milestone.objects.create(
            business=self.create_business(),
            milestone='Revenue Growth'
        )
        return milestone

    def create_covid_impact(self):
        impact = CovidImpact.objects.create(
            business=self.create_business(),
            impact_one='Loss of Customers',
            impact_two='Loss of Revenue'
        )
        return impact
