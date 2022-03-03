import json
from django_redis import get_redis_connection


def set_draft_application_data_to_redis_cache(application_id, data):
    """Sets application data to redis cache

    Args:
        application_id (int): the id for the application
        data (dictionary): the dict containing the database

    Returns:
        bool: status after setting
    """

    conn = get_redis_connection()
    application_data = conn.get(application_id)
    if not application_data:
        return conn.set(application_id, json.dumps(data))
    application_data = json.loads(application_data)
    application_data.update(data)
    return conn.set(application_id, json.dumps(application_data))


def get_draft_application_data_from_redis_cache(application_id):
    """Retrieves the application data from redis cache

    Args:
        application_id (int): the id of the application
    """

    conn = get_redis_connection()
    data = conn.get(application_id)
    if data:
        return json.loads(data)
    return {}


def delete_draft_application_data_from_redis_cache(application_id):
    conn = get_redis_connection()
    return conn.delete(application_id)
