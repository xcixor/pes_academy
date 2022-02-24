from django.views.generic import DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from application.presentation.views import (
    GetApplicationView, PostApplicationView)
from application.forms import ApplicationForm
from application.models import CallToAction, Application
from application.models import (
    BusinessOrganization, Milestone, CovidImpact)
from accounts.tests.common import AccountsBaseTestCase, User
from organization_subscription.models import OrganizationSubscription, Subscription


class ApplicationViewTestCase(AccountsBaseTestCase):

    def setUp(self):
        super(ApplicationViewTestCase, self).setUp()
        self.call_to_action = self.create_call_to_action_instance()
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

    def login_user(self):
        self.client.login(
            username=self.user.username, password='socrates123@')

    def test_get_application_view_properties(self):
        self.assertTrue(issubclass(GetApplicationView, DetailView))
        self.assertEqual(GetApplicationView.model, CallToAction)
        self.assertEqual(GetApplicationView.context_object_name, 'application')
        self.assertEqual(
            GetApplicationView.template_name, 'application/application_form.html')

    def test_post_application_view_properties(self):
        self.assertTrue(issubclass(PostApplicationView, FormView))
        self.assertTrue(issubclass(PostApplicationView, SingleObjectMixin))
        self.assertEqual(PostApplicationView.model, CallToAction)
        self.assertEqual(PostApplicationView.form_class, ApplicationForm)
        self.assertEqual(
            PostApplicationView.template_name, 'application/application_form.html')
        self.assertEqual(
            PostApplicationView.success_url, '/applications/')

    def test_gets_application_page_successfully(self):
        self.login_user()
        response = self.client.get(
            f'/applications/{self.call_to_action.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'application/application_form.html')

    def test_creates_application_if_user_does_not_have_one_or_a_subscription(self):
        self.assertEqual(Application.objects.count(), 0)
        self.login_user()
        self.client.get(
            f'/applications/{self.call_to_action.slug}/')
        self.assertEqual(Application.objects.count(), 1)

    def test_does_not_create_application_if_user_has_one(self):
        self.login_user()
        self.client.get(
            f'/applications/{self.call_to_action.slug}/')
        self.assertEqual(Application.objects.count(), 1)
        self.client.get(
            f'/applications/{self.call_to_action.slug}/')
        self.assertEqual(Application.objects.count(), 1)

    def test_does_not_create_application_if_user_has_a_subscription(self):
        organization_subscription = OrganizationSubscription.objects.create(
            subscription_creator=self.user
        )
        Subscription.objects.create(
            subscriber_email=self.user.email,
            subscription=organization_subscription
        )
        Application.objects.create(
            application_creator=self.user,
            call_to_action=self.call_to_action
        )
        self.login_user()
        self.client.get(
            f'/applications/{self.call_to_action.slug}/')
        self.assertEqual(Application.objects.count(), 1)
        self.client.get(
            f'/applications/{self.call_to_action.slug}/')
        self.assertEqual(Application.objects.count(), 1)

    def test_cannot_access_application_page_if_not_logged_in(self):
        response = self.client.get(
            f'/applications/{self.call_to_action.slug}/')
        self.assertRedirects(
            response,
            f'/accounts/login/?next=/applications/{self.call_to_action.slug}/',
            302)

    def test_adds_application_form_to_context(self):
        self.login_user()
        response = self.client.get(
            f'/applications/{self.call_to_action.slug}/')
        self.assertTrue(response.context['form'])

    def test_on_post_relevant_objects_created(self):
        self.login_user()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(BusinessOrganization.objects.count(), 0)
        self.assertEqual(CovidImpact.objects.count(), 0)
        self.assertIsNone(Milestone.objects.first().businesses.first())
        self.client.post(
            f'/applications/{self.call_to_action.slug}/', self.form_data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(BusinessOrganization.objects.count(), 1)
        self.assertEqual(CovidImpact.objects.count(), 1)
        self.assertEqual(Milestone.objects.first(
        ).businesses.first().organization_name, 'Big Tech')

    def test_redirects_on_successful_post(self):
        self.login_user()
        response = self.client.post(
            f'/applications/{self.call_to_action.slug}/',
            self.form_data, follow=True)
        self.assertRedirects(response, '/applications/', 302)

    def test_sets_success_message_on_successful_post(self):
        self.login_user()
        response = self.client.post(
            f'/applications/{self.call_to_action.slug}/',
            self.form_data, follow=True)
        message = list(response.context.get('messages'))[0]
        expected_message = (
            'Great, you application has been received. '
            'We will get back in touch with you.')
        self.assertEqual(message.tags, 'success')
        self.assertEqual(message.message, expected_message)

    def test_sets_error_message_on_post_form_error(self):
        self.login_user()
        self.form_data['age'] = 'nan'
        response = self.client.post(
            f'/applications/{self.call_to_action.slug}/',
            self.form_data, follow=True)
        message = list(response.context.get('messages'))[0]
        expected_message = (
            'An error occurred while validating your form. Please check that '
            'all fields are correct. Thank you.')
        self.assertEqual(message.tags, 'error')
        self.assertEqual(message.message, expected_message)
