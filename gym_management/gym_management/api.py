import frappe


@frappe.whitelist()
def book_class(session, member):
    booking = frappe.get_doc({
        "doctype": "Class Booking",
        "class_session": session,
        "member": member
    })

    booking.insert()

    return {
        "booking": booking.name,
        "status": booking.status
    }

@frappe.whitelist()
def get_available_sessions(date_from, date_to):
    sessions = frappe.get_all(
        "Class Session",
        filters={
            "session_date": ["between", [date_from, date_to]]
        },
        fields=[
            "name",
            "session_date",
            "start_datetime",
            "end_datetime",
            "gym_class",
            "capacity",
            "booked_count"
        ],
        order_by="session_date asc"
    )

    available_sessions = []

    for session in sessions:
        booked_count = session.booked_count or 0
        capacity = session.capacity or 0

        if booked_count < capacity:
            available_sessions.append(session)

    return available_sessions