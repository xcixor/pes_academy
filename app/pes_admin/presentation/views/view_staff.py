from django.contrib.auth import get_user_model
from django.views.generic import ListView


User = get_user_model()


class DisplayStaffView(ListView):

    template_name = 'pes_admin/view_staff.html'
    model = User
    context_object_name = 'staff'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_staff=True, is_superuser=False)
        return queryset
