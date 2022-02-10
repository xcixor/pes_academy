from datetime import datetime, timedelta, timezone
from common.tests.base_test_case import BaseTestCase
from application.models import Application


class ApplicationBaseTestCase(BaseTestCase):

    def setUp(self):
        super(ApplicationBaseTestCase, self).setUp()

    def create_application_instance(self):
        application = Application.objects.create(
            image=self.get_image(),
            tagline='Call For Application 1',
            description='Applications for agribusiness',
            slug='call-for-application-1',
            deadline=datetime.now(timezone.utc) + timedelta(days=10)
        )
        return application
