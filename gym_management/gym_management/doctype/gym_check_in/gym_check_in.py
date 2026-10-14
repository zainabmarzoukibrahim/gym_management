
# Copyright (c) 2026, zainab@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class GymCheckIn(Document):
    def validate(self):
        # Search about active membership of a member
        if self.member:
            membership = frappe.db.get_value(
                "Gym Membership",
                {
                    "member": self.member,
                    "status": "Active"
                },
                ["name", "start_date", "end_date"],
                as_dict=True
            )

            if not membership:
                frappe.throw(
                    "The member does not have an active membership"
                )

            # Date of check-in to check if membership is valid on it
            check_date = getdate(self.check_in_time)

            if check_date < getdate(membership.start_date):
                frappe.throw(
                    "The membership is not valid on the check-in date"
                )

            if (
                membership.end_date
                and check_date > getdate(membership.end_date)
            ):
                frappe.throw(
                    "The membership is not valid on the check-in date"
                )

            # Check freeze periods
            membership_doc = frappe.get_doc(
                "Gym Membership", membership.name
            )

            for freeze in membership_doc.freeze_history:
                if (
                    check_date >= getdate(freeze.freeze_from)
                    and check_date <= getdate(freeze.freeze_to)
                ):
                    frappe.throw(
                        "The membership is frozen on the check-in date"
                    )

            self.membership = membership_doc.name
            
            # Check the linked class booking
            if self.class_booking:
                booking = frappe.db.get_value(
                    "Class Booking",
                    self.class_booking,
                    ["member", "status"],
                    as_dict=True
                )

                if not booking:
                    frappe.throw("The class booking does not exist")

                if booking.member != self.member:
                    frappe.throw(
                        "The class booking belongs to another member"
                    )

                if booking.status != "Booked":
                    frappe.throw(
                        "Only booked class sessions can be checked in"
                    )
    
    def on_update(self):
        if self.class_booking:
            booking = frappe.get_doc(
                "Class Booking",
                self.class_booking
            )

            if booking.status == "Booked":
                booking.status = "Attended"
                booking.save()

