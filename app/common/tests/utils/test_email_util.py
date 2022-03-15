from django.core import mail
from django.test import TestCase
from common.utils.email import HtmlEmailMixin


class HtmlEmailMixinTestCase(TestCase):

    def send_email(self):
        HtmlEmailMixin().send_email(
            'Test email', None, 'email@test.com', ['receiver@recieve.com'])

    def test_can_send_email(self):
        self.send_email()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Test email')
        self.assertEqual(mail.outbox[0].to[0], 'receiver@recieve.com')

    def test_sends_html_email(self):
        self.send_email()
        content_type = mail.outbox[0].alternatives[0][1]
        self.assertEqual(content_type, 'text/html')

    def test_can_send_email_with_context(self):
        context = {'context': 'context object'}
        HtmlEmailMixin().send_email(
            'Test email', None, 'email@test.com', ['receiver@recieve.com'],
            context=context)
        sent_content = mail.outbox[0].alternatives[0][0]
        self.assertIn(context['context'], sent_content)

    def test_adds_logo_to_email_sent(self):
        self.send_email()
        sent_content = mail.outbox[0].alternatives[0][0]
        self.assertIn('cid:logo.webp', sent_content)
