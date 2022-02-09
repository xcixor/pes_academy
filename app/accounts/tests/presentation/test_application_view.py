from django.views.generic import DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from accounts.presentation.views import (
    GetApplicationView, PostApplicationView)
from accounts.forms.application_form import ApplicationForm
from sme.models import Application
from accounts.models import (
    User, BusinessOrganization, Milestone, CovidImpact)
from accounts.tests.common import AccountsBaseTestCase


class ApplicationViewTestCase(AccountsBaseTestCase):

    def setUp(self):
        super(ApplicationViewTestCase, self).setUp()
        self.application = self.create_application_instance()
        milestone = self.create_milestone()
        self.form_data = {
            'email': 'test@gmail.com',
            'full_name': 'Test Name',
            'age': 'range_one',
            'gender': 'male',
            'preferred_language': 'french',
            'organization_name': 'Big Tech',
            'facebook_link': 'https://www.facebook.com/bigtech',
            'value_chain': 'chain_three',
            'existence_period': 'period_two',
            'stage': 'stage_one',
            'impact': 'We beat it',
            'milestones': [milestone.id]
        }

    def test_get_application_view_properties(self):
        self.assertTrue(issubclass(GetApplicationView, DetailView))
        self.assertEqual(GetApplicationView.model, Application)
        self.assertEqual(GetApplicationView.context_object_name, 'application')
        self.assertEqual(
            GetApplicationView.template_name, 'application_form.html')

    def test_post_application_view_properties(self):
        self.assertTrue(issubclass(PostApplicationView, FormView))
        self.assertTrue(issubclass(PostApplicationView, SingleObjectMixin))
        self.assertEqual(PostApplicationView.model, Application)
        self.assertEqual(PostApplicationView.form_class, ApplicationForm)
        self.assertEqual(
            PostApplicationView.template_name, 'application_form.html')
        self.assertEqual(
            PostApplicationView.success_url, '/')

    def test_gets_application_page_successfully(self):
        response = self.client.get(
            f'/accounts/applications/{self.application.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'application_form.html')

    def test_on_post_relevant_objects_created(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(BusinessOrganization.objects.count(), 0)
        self.assertEqual(CovidImpact.objects.count(), 0)
        self.assertIsNone(Milestone.objects.first().businesses.first())
        self.client.post(
            f'/accounts/applications/{self.application.slug}/', self.form_data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(BusinessOrganization.objects.count(), 1)
        self.assertEqual(CovidImpact.objects.count(), 1)
        self.assertEqual(Milestone.objects.first(
        ).businesses.first().organization_name, 'Big Tech')

    def test_redirects_on_successful_post(self):
        response = self.client.post(
            f'/accounts/applications/{self.application.slug}/',
            self.form_data, follow=True)
        self.assertRedirects(response, '/', 302)

    def test_updates_application_applied_for_by_the_business(self):
        self.assertEqual(self.application.businesses.count(), 0)
        self.client.post(
            f'/accounts/applications/{self.application.slug}/', self.form_data)
        self.assertEqual(
            BusinessOrganization.objects.first().application, self.application)
        self.assertEqual(self.application.businesses.count(), 1)

    def test_sets_success_message_on_successful_post(self):
        response = self.client.post(
            f'/accounts/applications/{self.application.slug}/',
            self.form_data, follow=True)
        message = list(response.context.get('messages'))[0]
        expected_message = (
            'Great, you application has been received. '
            'We will get back in touch with you.')
        self.assertEqual(message.tags, 'success')
        self.assertEqual(message.message, expected_message)

    def test_sets_error_message_on_post_form_error(self):
        self.form_data['email'] = 'nan'
        response = self.client.post(
            f'/accounts/applications/{self.application.slug}/',
            self.form_data, follow=True)
        message = list(response.context.get('messages'))[0]
        expected_message = (
            'An error occurred while validating your form. Please check that '
            'all fields are correct. Thank you.')
        self.assertEqual(message.tags, 'error')
        self.assertEqual(message.message, expected_message)


    
