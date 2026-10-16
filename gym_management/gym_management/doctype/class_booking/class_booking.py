
# Copyright (c) 2026, zainab@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ClassBooking(Document):
    def validate(self):
        if self.member and self.is_new():
            #search about active membership of a member
            membership=frappe.db.get_value(
                "Gym Membership",
                {
                    "member":self.member,
                    "status":"Active"
                },
                ["name","start_date","end_date"],
                as_dict=True  #to return data in things that we can use like:membership.data
            )
            if not membership:
                frappe.throw("The member doesnot have an active membership")
            
            #date of session to check if the membership is valid on it
            session=frappe.db.get_value(
                "Class Session",self.class_session,"session_date"
            )
            if session < membership.start_date:
                frappe.throw("The membership is not valid on the session date")

            if membership.end_date and session > membership.end_date:
                frappe.throw("The membership is not valid on the session date")
            
            #check of freeze,because now we can get doc itself after we sure from it is exist
            membership_doc=frappe.get_doc("Gym Membership",membership.name)
            for freeze in membership_doc.freeze_history:
                if session>=freeze.freeze_from and session<= freeze.freeze_to:
                    frappe.throw("The membership is frozen on the session date")
                    
            self.membership=membership_doc.name

            #check of non dublicate class sission for same member
            existing_booking=frappe.db.exists(
                "Class Booking",
                {
                    "member":self.member,
                    "class_session":self.class_session,
                    "status":["!=","Cancelled"],
                    "name" : ["!=", self.name]#to allow editing
                }
            )
            if existing_booking:
                frappe.throw("You have already booked this class session")

            #checked for capacity
            if self.is_new():
                session_data=frappe.db.get_value(
                    "Class Session",
                    self.class_session,
                    ["capacity","booked_count"],
                    as_dict=True
                )
                if (session_data.booked_count or 0)>=session_data.capacity:
                    settings=frappe.get_single("Gym Settings")
                    if settings.enable_waitlist:
                        self.status="Waitlisted"
                    else:
                        frappe.throw("This class session is full")
                else:
                    self.status="Booked"

                    #update bookedcount

    def on_update(self):
        old_doc=self.get_doc_before_save()
        if old_doc:
            old_status=old_doc.status
        else:
            old_status=None
        new_status=self.status

        if old_status == new_status:
            return #same status->donot change

        if new_status == "Booked" and old_status != "Booked":
            frappe.db.set_value(
                "Class Session",
                self.class_session,
                "booked_count",
                (frappe.db.get_value(
                    "Class Session", self.class_session, "booked_count"
                ) or 0) + 1 #new value
            )

        elif old_status == "Booked" and new_status != "Booked":
            current_count=frappe.db.get_value(
                "Class Session",self.class_session,"booked_count"
            ) or 0

            frappe.db.set_value(
                "Class Session",
                self.class_session,
                "booked_count",
                max(0, current_count - 1)
            )

        # Promote the earliest waitlisted booking after cancellation
        if old_status == "Booked" and new_status == "Cancelled":
            next_booking = frappe.db.get_value(
                "Class Booking",
                {
                    "class_session": self.class_session,
                    "status": "Waitlisted"
                },
                "name",
                order_by="creation asc"
            )

            if next_booking:
                booking_doc = frappe.get_doc(
                    "Class Booking", next_booking
                )
                booking_doc.status = "Booked"
                booking_doc.save()

                member_email = frappe.db.get_value(
                    "Gym Member",
                    booking_doc.member,
                    "email"
                )

                if member_email:
                    frappe.sendmail(
                        recipients=[member_email],
                        subject="Your Gym Class Booking Is Confirmed",
                        message=(
                            "Good news! Your booking has been confirmed "
                            
                        )
                    )
