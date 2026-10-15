# Copyright (c) 2026, zainab@gmail.com and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase

class TestClassBooking(FrappeTestCase):
	
    def test_capacity_and_waitlist(self):
        gymroom = frappe.new_doc("Gym Room")
        gymroom.room_name = "test room"
        gymroom.capacity = 1
        gymroom.is_active = 1

        gymroom.insert()

        gymclass=frappe.new_doc("Gym Class")
        gymclass.class_name="test gymclass"
        gymclass.default_room=gymroom.name

        gymclass.insert()

        classsession=frappe.new_doc("Class Session")
        classsession.gym_class=gymclass.name
        classsession.session_date="2026-10-13"
        classsession.start_time="10:00:00"
        classsession.capacity=1
        classsession.room=gymroom.name
        classsession.status="Scheduled"

        classsession.insert()

        membershipplan = frappe.new_doc("Membership Plan")
        membershipplan.plan_name = "Test Plan"
        membershipplan.duration_type = "Days"
        membershipplan.duration_value = 1
        membershipplan.price = 100
        membershipplan.is_active = 1

        membershipplan.insert()

        gymmember1=frappe.new_doc("Gym Member")
        gymmember1.member_name="membe1r test"
        gymmember1.status="Active"

        gymmember1.insert()

        
        gymmember2=frappe.new_doc("Gym Member")
        gymmember2.member_name="member2 test"
        gymmember2.status="Active"
        gymmember2.insert()

        gymmembership1=frappe.new_doc("Gym Membership")
        gymmembership1.member=gymmember1.name
        gymmembership1.membership_plan=membershipplan.name
        gymmembership1.start_date="2026-10-12"
        gymmembership1.status="Active"
        gymmembership1.insert()

        gymmembership2=frappe.new_doc("Gym Membership")
        gymmembership2.member=gymmember2.name
        gymmembership2.membership_plan=membershipplan.name
        gymmembership2.start_date="2026-10-12"
        gymmembership2.status="Active"
        gymmembership2.insert()

        
        settings = frappe.get_single("Gym Settings")
        settings.enable_waitlist = 1
        settings.save()

        booking1=frappe.new_doc("Class Booking")
        booking1.class_session=classsession.name
        booking1.member=gymmember1.name
        booking1.membership=gymmembership1.name
        booking1.insert()

        
        booking2=frappe.new_doc("Class Booking")
        booking2.class_session=classsession.name
        booking2.member=gymmember2.name
        booking2.membership=gymmembership2.name
        booking2.insert()
        
        self.assertEqual(booking1.status, "Booked")
        self.assertEqual(booking2.status, "Waitlisted")