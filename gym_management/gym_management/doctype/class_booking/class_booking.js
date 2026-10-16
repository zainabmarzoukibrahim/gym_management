
 // Copyright (c) 2026, zainab@gmail.com and contributors
 // For license information, please see license.txt

frappe.ui.form.on("Class Booking", {
    setup(frm) {
        // Filter class_session to upcoming, non-cancelled sessions
        frm.set_query("class_session", function () {
            return {
                filters: [
                    ["session_date", ">=", frappe.datetime.get_today()],
                    ["status", "!=", "Cancelled"]
                ]
            };
        });
    },

    refresh(frm) {
        frm.trigger("update_remaining_spots");
    },

    class_session(frm) {
        frm.trigger("update_remaining_spots");
    },

    // Update remaining spots
    update_remaining_spots(frm) {
        if (!frm.doc.class_session) {
            frm.set_intro("");
            return;
        }

        frappe.db.get_value(
            "Class Session",
            frm.doc.class_session,
            ["capacity", "booked_count"]
        ).then(sessionresult => {
            let session = sessionresult.message;

            let remaining = Math.max(
                0,
                (session.capacity || 0) - (session.booked_count || 0)
            );

            if (remaining > 0) {
                frm.set_intro("Remaining spots: " + remaining, "green");
            } else {
                frm.set_intro("Remaining spots: " + remaining, "red");
            }
        });
    }
});
