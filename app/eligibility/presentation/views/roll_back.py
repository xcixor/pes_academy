from django.views.generic import DetailView
from application.models import Application
from agripitch.models import ApplicationMarks
from eligibility.models import BonusPoints, ShortListGroup


class RollBackApplicationView(DetailView):

    template_name = "profile/staff/applications.html"
    model = Application
    context_object_name = 'application'

    def get(self, request, *args, **kwargs):
        application = self.get_object()
        step = kwargs.get('step')
        application.stage = step
        application.disqualified = False
        application.save()
        current_step_slug = kwargs.get('current_step')
        current_step = None
        try:
            if current_step_slug == 'step_three':
                current_step = ShortListGroup.objects.get(group='step_two')
            else:
                current_step = ShortListGroup.objects.get(
                    group=current_step_slug)
            bonuses = BonusPoints.objects.filter(
                application=application, step=current_step)
            for bonus in bonuses:
                bonus.delete()
        except ShortListGroup.DoesNotExist as de:
            print(de)
        if current_step:
            for item in current_step.questions.all():
                try:
                    marks = ApplicationMarks.objects.filter(
                        question=item.question, application=self.get_object())
                    for mark in marks:
                        mark.delete()
                except ApplicationMarks.DoesNotExist as de:
                    print(de)
        return super().get(request, *args, **kwargs)
