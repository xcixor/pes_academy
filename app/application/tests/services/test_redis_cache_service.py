from django.test import TestCase
from django_redis import get_redis_connection
from application.services import (
    set_draft_application_data_to_redis_cache,
    get_draft_application_data_from_redis_cache,
    delete_draft_application_data_from_redis_cache)


class RedisCacheTestCase(TestCase):

    def setUp(self) -> None:
        self.data = {
            'company_name': 'Caravan Tech',
            'milestone': 'Gain customers'}

    def tearDown(self) -> None:
        get_redis_connection("default").flushall()

    def set_draft_application_data_to_redis_cache(self):
        return set_draft_application_data_to_redis_cache(1, self.data)

    def test_can_set_draft_application_data_to_redis_cache(self):

        status = self.set_draft_application_data_to_redis_cache()
        self.assertTrue(status)

    def test_can_get_draft_application_data_from_redis_cache(self):
        self.set_draft_application_data_to_redis_cache()
        data = get_draft_application_data_from_redis_cache('1')
        self.assertEqual(data['company_name'], 'Caravan Tech')

    def test_updates_if_similar_id(self):
        self.assertEqual(len(self.data), 2)
        self.set_draft_application_data_to_redis_cache()
        data = get_draft_application_data_from_redis_cache('1')
        self.assertEqual(data, self.data)
        self.data['age'] = 50
        self.data.pop('company_name')
        self.data.pop('milestone')
        self.assertEqual(len(self.data), 1)
        self.set_draft_application_data_to_redis_cache()
        updated_data = get_draft_application_data_from_redis_cache('1')
        self.assertEqual(updated_data['age'], 50)
        self.assertEqual(updated_data['company_name'], 'Caravan Tech')
        self.assertEqual(updated_data['milestone'], 'Gain customers')

    def test_deletes_application_from_cache(self):
        self.set_draft_application_data_to_redis_cache()
        status = delete_draft_application_data_from_redis_cache('1')
        self.assertTrue(status)
