# Copyright (c) 2026, zainab@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today, getdate


class GymMember(Document):
    def validate(self):
        date_of_birth=self.date_of_birth
        if date_of_birth and getdate(date_of_birth)>getdate(today()):
            frappe.throw("Date Of Birth Canot Be In The Future")
        if not self.customer:
            customer = frappe.new_doc("Customer")
            customer.customer_name=self.member_name
            customer.customer_type="Individual"
            customer.customer_group = "Individual"
            customer.insert()
            self.customer=customer.name
