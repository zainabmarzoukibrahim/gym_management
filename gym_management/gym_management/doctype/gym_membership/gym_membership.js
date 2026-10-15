frappe.ui.form.on("Gym Membership", {
    refresh(frm) {
        // Membership Status Colors
        if (frm.doc.status) {
            const status_colors = {
                "Draft": "gray",
                "Active": "green",
                "Frozen": "blue",
                "Expired": "red",
                "Cancelled": "gray"
            };

            frm.page.set_indicator(
                frm.doc.status,
                status_colors[frm.doc.status] || "gray"
            );
        }
        let sub=frm.doc.docstatus===1;//submitted
        let done = frm.doc.status === "Expired" || frm.doc.status === "Cancelled";
        

        frm.toggle_display("sales_invoice", sub)
        frm.toggle_display("freeze_history", sub);
        
  
        // Freeze Membership
        if (frm.doc.docstatus === 1 && frm.doc.status === "Active" && !frm.is_new()) {
            frm.add_custom_button("Freeze", () => {
                frappe.prompt(
                    [
                        {
                            label: "Freeze From",
                            fieldname: "freeze_from",
                            fieldtype: "Date",
                            reqd: 1
                        },
                        {
                            label: "Freeze To",
                            fieldname: "freeze_to",
                            fieldtype: "Date",
                            reqd: 1
                        },
                        {
                            label: "Reason",
                            fieldname: "reason",
                            fieldtype: "Small Text",
                            reqd: 0
                        }
                    ],
                    (values) => {
                        frm.call("freeze_membership", {
                            freeze_from: values.freeze_from,
                            freeze_to: values.freeze_to,
                            reason: values.reason
                        }).then(() => {
                            frappe.show_alert({
                                message: "Membership frozen successfully",
                                indicator: "green"
                            });
                            frm.reload_doc();
                        });
                    },
                    "Freeze Membership",
                    "Confirm"
                );
            });
        }

        // Renew Membership
        if (frm.doc.docstatus === 1 && frm.doc.status === "Expired" && !frm.is_new()) {
            frm.add_custom_button("Renew", () => {
                frappe.confirm(
                    "Are you sure you want to renew this membership?",
                    () => {
                        frm.call("renew_membership").then((r) => {
                            if (r.message) {
                                frappe.msgprint(
                                    "New membership created: " + r.message
                                );
                                frm.reload_doc();
                            }
                        });
                    }
                );
            });
        }
    },
    //ظهور class remaining لو الduration type كان class pack
    membership_plan(frm) {
        frappe.db.get_value(
            "Membership Plan",
            frm.doc.membership_plan,
            "duration_type"
        ).then(pack => {
            frm.toggle_display(
                "classes_remaining",
                pack.message.duration_type === "Class Pack"
            );
        });
    }
});
