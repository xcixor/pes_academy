from django.views.generic import CreateView
from application.models import QuestionComment


class QuestionCommentView(CreateView):

    model = QuestionComment
    template_name = 'eligibility/eligibility.html'
    fields = '__all__'

    def get_success_url(self) -> str:
        slug = self.kwargs.get('slug')
        return f'/eligibility/{slug}/'
