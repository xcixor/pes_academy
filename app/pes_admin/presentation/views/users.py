from django.views.generic import ListView
from django.contrib.auth import get_user_model

User = get_user_model()


class AllUsersView(ListView):

    template_name = 'pes_admin/users_all.html'
    model = User
    context_object_name = 'users'
    paginate_by = 50

    def get_queryset(self):
        return super().get_queryset().filter(is_staff=False)


class RegularUsers(ListView):

    template_name = 'pes_admin/users_regular.html'
    model = User
    context_object_name = 'users'
    paginate_by = 50

    def get_queryset(self):
        return super().get_queryset().filter(
            is_applying_for_a_call_to_action=False)


class CallToActionUsers(ListView):

    template_name = 'pes_admin/users_call_to_action.html'
    model = User
    context_object_name = 'users'
    paginate_by = 50

    def get_queryset(self):
        return super().get_queryset().filter(
            is_applying_for_a_call_to_action=True)
