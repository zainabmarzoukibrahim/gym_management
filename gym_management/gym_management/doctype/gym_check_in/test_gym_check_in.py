# Copyright (c) 2026, zainab@gmail.com and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import add_days, today


class TestGymCheckIn(FrappeTestCase):

    def test_expired_membership_check_in_blocked(self):
        member = frappe.new_doc("Gym Member")
        member.member_name = "Test Expired Member"
        member.insert()

        plan = frappe.new_doc("Membership Plan")
        plan.plan_name = "Test Expired Plan"
        plan.duration_type = "Days"
        plan.duration_value = 30
        plan.price = 100
        plan.is_active = 1
        plan.insert()

        membership = frappe.new_doc("Gym Membership")
        membership.member = member.name
        membership.membership_plan = plan.name
        membership.start_date = add_days(today(), -60)
        membership.end_date = add_days(today(), -1)
        membership.status = "Expired"
        membership.insert()

        check_in = frappe.new_doc("Gym Check In")
        check_in.member = member.name
        check_in.check_in_time = today()

        with self.assertRaises(frappe.ValidationError):
            check_in.insert()
