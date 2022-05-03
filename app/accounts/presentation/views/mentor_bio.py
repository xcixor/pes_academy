from django.contrib.auth import get_user_model
from django.views.generic import DetailView

User = get_user_model()


class MentorBio(DetailView):

    model = User
    template_name = 'profile/mentor_bio.html'
    context_object_name = 'mentor'
