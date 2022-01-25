from django.shortcuts import render
from django.views.generic import TemplateView


class ApplicationView(TemplateView):
    template_name = "application_form.html"