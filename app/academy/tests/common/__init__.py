from common.tests.base_test_case import BaseTestCase
from academy.models import Session, Meeting


class AcademyBaseTestCase(BaseTestCase):

    def create_session(self):
        coach = self.create_logged_in_admin()
        coachee = self.create_normal_user()
        session = Session.objects.create(
            coach=coach,
            coachee=coachee,
            title='Induction',
            description='To introduce client to session'
        )
        return session

    def create_meeting(self):
        session = self.create_session()
        meeting = Meeting.objects.create(
            session=session,
            link='https://calendly.com/test_calender/introduction-to-marketing'
        )
        return meeting
