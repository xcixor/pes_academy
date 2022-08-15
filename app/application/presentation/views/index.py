from django.views.generic import ListView
from django.utils import timezone
from application.models import CallToAction, CarouselImage


class IndexView(ListView):

    template_name = "index/index.html"
    model = CallToAction
    context_object_name = 'calls_to_action'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            available_for_applications=True,
            deadline__gte=timezone.now())
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if CarouselImage.objects.all():
            first_image = CarouselImage.objects.first()
            context['first_carousel_image'] = first_image
            context['other_carousel_images'] = CarouselImage.objects.exclude(
                id=first_image.id)
        return context
