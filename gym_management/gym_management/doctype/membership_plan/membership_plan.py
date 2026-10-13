# Copyright (c) 2026, zainab@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MembershipPlan(Document):
    def validate(self):
        if self.price < 0:
            frappe.throw("Price Canot Be Negative")
        if self.duration_value is not None and self.duration_value <= 0:
            frappe.throw("Duration Value Canot Be Zero Or Less")
        if not self.item:
            item=frappe.new_doc("Item")
            item.item_code=self.plan_name
            item.item_group="Services"
            item.default_unit_of_measure = "Nos"
            item.is_stock_item = 0
            item.insert()
            self.item=item.name
        item_price_name=frappe.db.get_value(
            "Item Price",
            {
                "item_code":self.item,
                "price_list": "Standard Selling"
            },
            "name"
        )
        if item_price_name:
            item_price=frappe.get_doc("Item Price",item_price_name)
            item_price.price_list_rate=self.price
            item_price.save()
        else:
                item_price=frappe.new_doc("Item Price")
                item_price.item_code=self.item
                item_price.price_list="Standard Selling"
                item_price.price_list_rate=self.price
                item_price.insert()
