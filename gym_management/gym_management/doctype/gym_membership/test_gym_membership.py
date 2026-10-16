# Copyright (c) 2026, zainab@gmail.com and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestGymMembership(FrappeTestCase):
    def test_membership_without_member(self):
        plan = frappe.new_doc("Membership Plan")
        plan.plan_name = "Test Plan"
        plan.duration_type = "Months"
        plan.duration_value = 1
        plan.price = 100
        plan.is_active = 1

        plan.insert()
        
        membership = frappe.new_doc("Gym Membership")
        membership.membership_plan = plan.name
        membership.start_date="14-10-2026"
        with self.assertRaises(frappe.MandatoryError):
            membership.insert()
    def test_freeze_days_exceed_limit(self):
        plan = frappe.new_doc("Membership Plan")
        plan.plan_name = "Freeze Test Plan"
        plan.duration_type = "Months"
        plan.duration_value = 1
        plan.price = 100
        plan.max_freeze_days = 5

        plan.insert()

        membership = frappe.new_doc("Gym Membership")
        membership.membership_plan = plan.name

        membership.append("freeze_history", {
            "freeze_from": "2026-10-01",
            "freeze_to": "2026-10-10"
        })


        with self.assertRaises(frappe.ValidationError):
             membership.insert()