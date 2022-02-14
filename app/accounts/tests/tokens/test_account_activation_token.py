from django.contrib.auth import get_user_model
from accounts.tokens import account_activation_token
from accounts.tests.common import AccountsBaseTestCase


class AccountActivationTokenTestCase(AccountsBaseTestCase):

    def setUp(self) -> None:
        super(AccountActivationTokenTestCase, self).setUp()

    def test_generates_valid_token(self):
        user = get_user_model().objects._create_user(
            'test@gmail.com', 'password')
        token = account_activation_token.make_token(user)
        self.assertTrue(token)
        self.assertTrue(account_activation_token.check_token(user, token))
