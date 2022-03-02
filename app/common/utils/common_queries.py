from organization_subscription.models import Subscription


def get_application(user):
    application = None
    msg = None
    try:
        application = user.application
    except AttributeError as ae:
        msg = ae
    if not application:
        subscription = None
        try:
            subscription = Subscription.objects.get(
                subscriber_email=user.email)
        except Subscription.DoesNotExist as sd:
            msg = sd
        if subscription:
            try:
                application = subscription.subscription.subscription_creator.application
            except AttributeError as ae:
                msg = ae
    return application, msg
