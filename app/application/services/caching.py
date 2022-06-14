from application.models import ApplicationDraftData


def set_draft_application_data_to_cache(application, data):
    """Sets application data to cache

    Args:
        application_id (int): the id for the application
        data (dictionary): the dict containing the database

    Returns:
        bool: status after setting
    """
    application, created = ApplicationDraftData.objects.get_or_create(
        application=application)
    ApplicationDraftData.objects.filter(pk=application.pk).update(**data)
    return created


def get_draft_application_data_from_cache(application):
    """Retrieves the application data from cache

    Args:
        application_id (int): the id of the application
    """
    data = {}
    application_found = None
    try:
        application_found = ApplicationDraftData.objects.get(
            application=application)
    except ApplicationDraftData.DoesNotExist as exc:
        print(exc)
    if application_found:
        data = ApplicationDraftData.objects.filter(pk=application_found.pk).values()
    return data[0]


def delete_draft_application_data_from_cache(application):
    return ApplicationDraftData.objects.get(application=application).delete()
