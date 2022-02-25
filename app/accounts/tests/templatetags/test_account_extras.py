from accounts.tests.common import AccountsBaseTestCase
from accounts.templatetags.account_extras import get_profile


class AccountExtrasTestCase(AccountsBaseTestCase):

    def setUp(self):
        super(AccountExtrasTestCase, self).setUp()

    def test_can_get_profile(self):
        self.assertTrue(get_profile(self.user.email))
