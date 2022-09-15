from django.views.generic import CreateView
from django.contrib import messages
from agripitch.models import SubCriteriaItemFieldProperties
from agripitch.forms import SubCriteriaItemFieldPropertiesForm


class SubCriteriaItemFieldPropertiesView(CreateView):

    model = SubCriteriaItemFieldProperties
    template_name = 'pes_admin/subcriteria_item_properties.html'
    form_class = SubCriteriaItemFieldPropertiesForm
    success_url = '/admin/advanced/create/subcriteria/property/'

    NAME_CHOICES = [
        'class',
        'accept',
        'max_size',
        'required',
        'min',
        'max'
    ]
    VALUE_CHOICES = (
        'form-input-validate',
        'form-radio',
        'form-input-validate form-radio',
        '.pdf',
        'image/*'
        '1048576',
        '2097152',
        'False',
        '1987-01-01',
        '2004-01-01',
        'form-input-validate form-radio multiple_checkbox'
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_choices'] = self.NAME_CHOICES
        context['value_choices'] = self.VALUE_CHOICES
        return context

    def form_valid(self, form):
        success_message = "Great your property has been added"
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        error_message = "Error. Please correct the errors in your form"
        messages.add_message(
            self.request, messages.SUCCESS, error_message)
        return super().form_invalid(form)
