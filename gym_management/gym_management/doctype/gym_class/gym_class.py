# Copyright (c) 2026, zainab@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class GymClass(Document):
    def validate(self):
        if self.default_room:
            room=frappe.get_doc("Gym Room",self.default_room)

            if self.default_capacity is not None and self.default_capacity > room.capacity:
                frappe.throw(  "Default Capacity cannot exceed Room Capacity"   )

