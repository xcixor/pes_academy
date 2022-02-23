from django.contrib.auth import get_user_model
from application.tests.common import ApplicationBaseTestCase
from application.models import BusinessOrganization, Milestone, CovidImpact
from application.models import Application


User = get_user_model()


class AccountsBaseTestCase(ApplicationBaseTestCase):

    def setUp(self):
        super(AccountsBaseTestCase, self).setUp()
        self.user = self.create_user()

    def create_user(self):
        user = self.create_normal_user()
        user.email = 'test@gmail.com'
        user.is_active = True
        user.save()
        return user

    def create_application(self):
        application = Application.objects.create(
            application_creator=self.user,
            call_to_action=self.create_call_to_action_instance()
        )
        return application

    def create_business(self):
        link = BusinessOrganization.objects.create(
            organization_owner=self.user,
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
