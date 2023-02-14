from django.conf import settings
from common.models import PartnerLogo


def logos(request):
    return {'logos': PartnerLogo.objects.all()}


def debug_context(request):
    debug_flag = settings.DEBUG
    return{"debug_flag": debug_flag}
