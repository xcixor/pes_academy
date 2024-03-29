from .help import HelpView
from .registration import (
    GetRegistrationView, PostRegistrationView,
    RegistrationView, ReviewerRegistrationView)
from .login import UserLoginView
from .activate_account import ActivationEmailSentView, AccountActivationView
from .dashboard import DashboardView
from .staff.applications import ApplicationsToReviewView
from .mentor_bio import CoachBio
from .coaching import Coaching, CoachSessions, SessionView
from .profile import ViewProfile, EditProfile
from .password_change import PasswordChangeView, PasswordResetView
from .resend_activation_email import ResendActivationEmailView
