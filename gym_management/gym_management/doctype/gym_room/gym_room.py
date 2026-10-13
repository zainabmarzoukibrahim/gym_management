# Copyright (c) 2026, zainab@gmail.com and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document


class GymRoom(Document):
    def validate(self):
        if not self.room_name:
            frappe.throw("Room Name is required")

        if self.capacity is None or self.capacity <= 0:
            frappe.throw("Capacity must be greater than zero")
