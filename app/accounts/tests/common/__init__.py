from django.contrib.auth import get_user_model
# from application.tests.common import ApplicationBaseTestCase
# from application.models import BusinessOrganization, Milestone, CovidImpact
# from application.models import Application
from common.tests.base_test_case import BaseTestCase


User = get_user_model()


class AccountsBaseTestCase(BaseTestCase):

    def setUp(self):
        super(AccountsBaseTestCase, self).setUp()
        self.user = self.create_user()

    def create_user(self):
        user = self.create_normal_user()
        user.email = 'test@gmail.com'
        user.is_active = True
        user.save()
        return user

