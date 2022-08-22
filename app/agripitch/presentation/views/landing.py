from django.views.generic import TemplateView
from application.models import CallToAction, CarouselImage


class AgripitchLandingView(TemplateView):

    template_name = "agripitch/landing.html"
    context_object_name = 'calls_to_action'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if CarouselImage.objects.all():
            first_image = CarouselImage.objects.first()
            context['first_carousel_image'] = first_image
            context['other_carousel_images'] = CarouselImage.objects.exclude(
                id=first_image.id)
        context['application'] = CallToAction.objects.first()
        return context
