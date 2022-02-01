from django.contrib.admin.sites import AdminSite
from accounts.models import User, BusinessOrganization, Milestone, CovidImpact
from accounts.admin import (
    BusinessOrganizationInline, UserAdmin,
    BusinessOrganizationAdmin, MilestoneInline, CovidImpactInline)
from accounts.tests.common import AccountsBaseTestCase


class UserAdminTestCase(AccountsBaseTestCase):

    def setUp(self):
        super(UserAdminTestCase, self).setUp()
        self.model_admin = UserAdmin(
            model=User,
            admin_site=AdminSite
        )
        self.model_admin.save_model(
            obj=self.create_user(),
            request=self.create_logged_in_admin(),
            form=None,
            change=None
        )

    def test_inline_properties(self):
        self.assertEqual(self.model_admin.model, User)
        list_display = ['full_name', 'email_address', 'date_joined']
        inlines = [BusinessOrganizationInline]
        self.assertEqual(self.model_admin.list_display, list_display)
        self.assertEqual(self.model_admin.inlines, inlines)

    def test_inlines_properties(self):
        inline = self.model_admin.inlines[0]
        self.assertEqual(inline.model, BusinessOrganization)
        self.assertEqual(inline.extra, 0)


class BusinessOrganizationAdminTestCase(AccountsBaseTestCase):

    def setUp(self):
        super(BusinessOrganizationAdminTestCase, self).setUp()
        self.model_admin = BusinessOrganizationAdmin(
            model=BusinessOrganization,
            admin_site=AdminSite
        )
        self.model_admin.save_model(
            obj=self.create_business(),
            request=self.create_logged_in_admin(),
            form=None,
            change=None
        )

    def test_inline_properties(self):
        self.assertEqual(self.model_admin.model, BusinessOrganization)
        list_display = ['organization_name', 'organization_owner']
        inlines = [CovidImpactInline]
        self.assertEqual(self.model_admin.list_display, list_display)
        self.assertEqual(self.model_admin.inlines, inlines)

    def test_inlines_properties(self):
        inline = self.model_admin.inlines[0]
        self.assertEqual(inline.model, CovidImpact)
        self.assertEqual(inline.extra, 0)
