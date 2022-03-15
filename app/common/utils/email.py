import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
from django.conf import settings


class HtmlEmailMixin(object):

    def send_email(self, *args, **kwargs):
        """Send html email.
        args sequence - subject, body, from_email, to_emails
        """
        subject, body, from_email, to_emails = args
        root_dir = str(settings.BASE_DIR)[:-4]
        img_dir = root_dir + 'common/static/common/images/'
        image = 'logo.webp'
        file_path = os.path.join(img_dir, image)
        with open(file_path, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', '<{name}>'.format(name=image))
            img.add_header('cid', '<{name}>'.format(name=image))
            img.add_header('Content-Disposition', 'inline', filename=image)
        email_message = EmailMultiAlternatives(
            subject, body, from_email, to_emails
        )
        html_content = render_to_string(
            kwargs.get(
                'template', 'common/email/base.html'), kwargs.get('context', None)
        )
        email_message.attach_alternative(html_content, 'text/html')
        email_message.attach(img)
        email_message.send()
