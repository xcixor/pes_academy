from django.test import TestCase
from django_redis import get_redis_connection
from application.services import (
    set_draft_application_data_to_cache,
    get_draft_application_data_from_cache,
    delete_draft_application_data_from_cache)
from application.tests.common import ApplicationBaseTestCase
from application.models import ApplicationDraftData


class CacheTestCase(ApplicationBaseTestCase):

    def setUp(self) -> None:
        super(CacheTestCase, self).setUp()
        self.data = {
            'organization_name': 'Caravan Tech',
            'milestones': 'Gain customers'}
        self.application = self.create_application_instance()

    def tearDown(self) -> None:
        get_redis_connection("default").flushall()

    def set_draft_application_data_to_cache(self):
        return set_draft_application_data_to_cache(self.application, self.data)

    def test_can_set_draft_application_data_to_cache(self):

        status = self.set_draft_application_data_to_cache()
        self.assertTrue(status)

    def test_can_get_draft_application_data_from_cache(self):
        self.set_draft_application_data_to_cache()
        data = get_draft_application_data_from_cache(self.application)
        self.assertEqual(data['organization_name'], 'Caravan Tech')

    def test_deletes_application_from_cache(self):
        self.set_draft_application_data_to_cache()
        status = delete_draft_application_data_from_cache(self.application)
        self.assertTrue(status)
