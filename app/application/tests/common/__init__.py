from datetime import datetime, timedelta, timezone
from common.tests.base_test_case import BaseTestCase
from application.models import (
    CallToAction, Application, ApplicationDocument)


class ApplicationBaseTestCase(BaseTestCase):

    def setUp(self):
        super(ApplicationBaseTestCase, self).setUp()

    def create_call_to_action_instance(self):
        call_to_action = CallToAction.objects.create(
            image=self.get_image(),
            tagline='Call For Application 1',
            description='Applications for agribusiness',
            slug='call-for-application-1',
            deadline=datetime.now(timezone.utc) + timedelta(days=10),
            available_for_applications=True
        )
        return call_to_action

    def create_application_instance(self):
        application = Application.objects.create(
            application_creator=self.create_normal_user(),
            call_to_action=self.create_call_to_action_instance()
        )
        return application

    def create_application_document(self):
        application = self.create_application_instance()
        document = ApplicationDocument.objects.create(
            document_name='KRA Pin',
            document=self.get_image(),
            application=application
        )
        return document
