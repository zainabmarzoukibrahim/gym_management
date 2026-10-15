import frappe
from frappe.utils import add_days, getdate, today,get_datetime,now_datetime


def process_membership_expiry():
    today_date = getdate(today())

    # Expire memberships whose end date has passed
    expired_memberships = frappe.get_all(
        "Gym Membership",
        filters={
            "docstatus": 1,
            "status": ["in", ["Active", "Frozen"]],
            "end_date": ["<", today_date]
        },
        pluck="name"
    )

    for membership_name in expired_memberships:
        frappe.db.set_value(
            "Gym Membership",
            membership_name,
            "status",
            "Expired"
        )

    # Get the configured reminder period
    settings = frappe.get_single("Gym Settings")
    reminder_days = settings.expiry_reminder_days or 0

    if reminder_days <= 0:
        return

    reminder_date = add_days(today_date, reminder_days)

    # Find active memberships expiring on the reminder date
    expiring_memberships = frappe.get_all(
        "Gym Membership",
        filters={
            "docstatus": 1,
            "status": "Active",
            "end_date": reminder_date
        },
        fields=["name", "member", "end_date"]
    )

    for membership in expiring_memberships:
        member_email = frappe.db.get_value(
            "Gym Member",
            membership.member,
            "email"
        )

        if not member_email:
            continue

        frappe.sendmail(
            recipients=[member_email],
            subject="Your Gym Membership Is Expiring Soon",
            message=(
                f"Your gym membership {membership.name} "
                f"will expire on {membership.end_date}. "
                "Please renew your membership if you wish to continue."
            )
        )

#cancel_expired_bookings
def cancel_expired_bookings():
    current_datetime = now_datetime()
    sessions=frappe.get_all(
        "Class Session",
        filters={
            "status":"Scheduled",
            "session_date":["<=",getdate(current_datetime)]
        },fields=["name","session_date","end_time"]
    )
    for session in sessions:
        sessionend=get_datetime(str(session.session_date)+" " +str(session.end_time))
        
        if( sessionend <= current_datetime ):
            bookings = frappe.get_all(
                "Class Booking",
                filters={
                    "class_session": session.name,
                    "status": ["in", ["Booked", "Waitlisted"]]
            },
                pluck="name"
        )
            for booking_name in bookings:
                frappe.db.set_value(
                    "Class Booking",
                     booking_name,
                     {
                         "status": "Cancelled",
                         "cancelled_on": current_datetime
                     }
            )
            frappe.db.set_value("Class Session", session.name, "status", "Completed")


