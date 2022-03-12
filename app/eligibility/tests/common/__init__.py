from datetime import datetime, timedelta, timezone
from django.contrib.auth.models import Group, Permission
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from common.tests.base_test_case import BaseTestCase
from application.models import (CallToAction, Application)


class StaffBaseTestCase(BaseTestCase):

    def setUp(self) -> None:
        super(StaffBaseTestCase, self).setUp()
        self.user = self.create_normal_user()
        self.admin = self.create_logged_in_admin()

    def create_call_to_action_instance(self):
        call_to_action = CallToAction.objects.create(
            image=self.get_image(),
            tagline='Call For Application 1',
            description='Applications for agribusiness',
            slug='call-for-application-1',
            deadline=datetime.now(timezone.utc) + timedelta(days=10)
        )
        return call_to_action

    def create_application_instance(self):
        creator = get_user_model().objects.create_temporal_user(
            'new_user@gmail.com')
        application = Application.objects.create(
            application_creator=creator,
            call_to_action=self.create_call_to_action_instance()
        )
        return application
