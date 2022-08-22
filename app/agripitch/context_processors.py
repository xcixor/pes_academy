from agripitch.models import PartnerLogo


def logos(request):
    return {'logos': PartnerLogo.objects.all()}
