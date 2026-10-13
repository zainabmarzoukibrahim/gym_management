# Copyright (c) 2026, zainab@gmail.com and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document


class GymTrainer(Document):
    def validate(self):
        if not self.employee:
            frappe.throw("Employee is required")

        if not self.trainer_name:
            frappe.throw("Trainer Name is required")
