from django.views.generic import ListView
from django.contrib.auth import get_user_model

User = get_user_model()


class AllUsersView(ListView):

    template_name = 'pes_admin/users_all.html'
    model = User
    context_object_name = 'users'

    def get_queryset(self):
        return super().get_queryset().filter(is_staff=False)
