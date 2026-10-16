# Copyright (c) 2026, zainab@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_days, add_months, getdate, date_diff


class GymMembership(Document):
    def validate(self):
        if not self.start_date:
            frappe.throw("Start Date Is Required")

        if not self.membership_plan:
            frappe.throw("Membership Plan Is Required")
        #getting deatils of plan from membership
        plan=frappe.get_doc(
            "Membership Plan",
            self.membership_plan
        )
        #calculate end date based on plan
        if plan.duration_type=="Days":
            self.end_date=add_days(
                getdate(self.start_date),plan.duration_value
            )
            self.classes_remaining = 0

        elif plan.duration_type=="Months":
            self.end_date=add_months(
                getdate(self.start_date),plan.duration_value
            )
            self.classes_remaining = 0

        elif plan.duration_type=="Class Pack":
            self.end_date=None
            if self.is_new():
                self.classes_remaining = plan.duration_value

        #ensure that a member doesnot have more than one membership
        if self.member and self.status=="Active":
            existing_membership=frappe.db.exists(
                "Gym Membership",
                {
                    "member":self.member,
                    "status":"Active",
                    "name":["!=",self.name or""],
                    "docstatus":1
                }
            )
            if existing_membership:
                frappe.throw("This member already has an active membership")

        self.check_freeze()  

    
    def check_freeze(self):
        membershipplan = frappe.get_doc("Membership Plan", self.membership_plan)
        totalfreeze = 0
        for record in self.freeze_history:
            freezefrom = getdate(record.freeze_from)
            freezeto = getdate(record.freeze_to)
            if freezeto <= freezefrom:
                frappe.throw("Freeze to must be after Freeze from")
            record.days = date_diff(freezeto, freezefrom) + 1
            totalfreeze = totalfreeze + record.days
        if totalfreeze > (membershipplan.max_freeze_days or 0):
            frappe.throw("Total freeze days exceed the maximum allowed")

    
    def before_update_after_submit(self):
        self.check_freeze()

    #create invoice on submit
    def on_submit(self):
        #donot dublicate
        frappe.db.set_value("Gym Member", self.member, "active_membership", self.name)
        if self .sales_invoice and frappe.db.exists(
            "Sales Invoice",self.sales_invoice
        ):
            return
        member =frappe.get_doc("Gym Member",self.member)

        if not member.customer:
            frappe.throw ("this member has no linked customer")

        mimbershipplan=frappe.get_doc(
            "Membership Plan",self.membership_plan
        )

        if not mimbershipplan.item:
            frappe.throw("This Membership Plan has no linked Item")

        company=frappe.defaults.get_user_default("Company")
        if not company:
            frappe.throw("please set a default company first")

        invoice= frappe.new_doc("Sales Invoice")
        invoice.customer=member.customer
        invoice.company=company
        invoice.append("items", {
            "item_code": mimbershipplan.item,
            "qty": 1,
            "rate": mimbershipplan.price
        })
        invoice.set_missing_values()
        invoice.calculate_taxes_and_totals()

        invoice.insert()
        invoice.submit()
        self.db_set("sales_invoice", invoice.name)

    def on_cancel(self):
        frappe.db.set_value("Gym Member", self.member, "active_membership", None)
        self.db_set("status", "Cancelled")
        if not self.sales_invoice:
            return

        if not frappe.db.exists("Sales Invoice", self.sales_invoice):
            return

        invoice = frappe.get_doc("Sales Invoice", self.sales_invoice)

        # Nothing to cancel if the invoice is already cancelled
        if invoice.docstatus == 2:
            return

        # Cancel only submitted invoices
        if invoice.docstatus != 1:
            return

        invoice.cancel()


    @frappe.whitelist()
    def renew_membership(self):
        if self.docstatus != 1:
            frappe.throw("Only submitted memberships can be renewed")

        if self.status != "Expired":
            frappe.throw("Only expired memberships can be renewed")

        new_membership = frappe.new_doc("Gym Membership")
        new_membership.member = self.member
        new_membership.membership_plan = self.membership_plan
        new_membership.start_date = frappe.utils.today()
        new_membership.status = "Active"

        new_membership.insert()
        new_membership.submit()

        return new_membership.name

    #freeze membership
    @frappe.whitelist()
    def freeze_membership(self, freeze_from, freeze_to, reason=None):
        if self.status!="Active":
            frappe.throw("Only active memberships can be frozen")

       
        self.append("freeze_history", {
             "freeze_from": getdate(freeze_from),
             "freeze_to": getdate(freeze_to),
             "reason": reason
        })
        self.status = "Frozen"
        self.save()