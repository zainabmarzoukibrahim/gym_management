# Copyright (c) 2026, zainab@gmail.com and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document


class GymSettings(Document):
    def validate(self):
        if self.cancellation_window_hours is not None:
            if self.cancellation_window_hours < 0:
                frappe.throw("Cancellation Window Hours cannot be negative")

        if self.no_show_limit is not None:
            if self.no_show_limit < 0:
                frappe.throw("No Show Limit cannot be negative")

        if self.expiry_reminder_days is not None:
            if self.expiry_reminder_days < 0:
                frappe.throw("Expiry Reminder Days cannot be negative")
