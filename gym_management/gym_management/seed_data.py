
import frappe
from frappe.utils import add_days, today


def get_or_create(doctype, filters, values):
    """Return an existing record or create it."""
    existing = frappe.db.get_value(doctype, filters, "name")

    if existing:
        return existing

    doc = frappe.new_doc(doctype)
    doc.update(values)
    doc.insert(ignore_permissions=True)
    return doc.name


def create_plan(plan_name, item_code, duration_type, duration_value,
                price, max_freeze_days, classes_included=0):
    plan_name_existing = frappe.db.get_value(
        "Membership Plan", {"plan_name": plan_name}, "name"
    )

    if plan_name_existing:
        return plan_name_existing

    # Create the Item explicitly so its required UOM is set.
    item_name = frappe.db.get_value(
        "Item", {"item_code": item_code}, "name"
    )

    if not item_name:
        item = frappe.new_doc("Item")
        item.item_code = item_code
        item.item_name = plan_name
        item.item_group = "Services"
        item.stock_uom = "Nos"
        item.is_stock_item = 0
        item.insert(ignore_permissions=True)
        item_name = item.name

    plan = frappe.new_doc("Membership Plan")
    plan.plan_name = plan_name
    plan.item = item_name
    plan.duration_type = duration_type
    plan.duration_value = duration_value
    plan.price = price
    plan.max_freeze_days = max_freeze_days
    plan.classes_included = classes_included
    plan.is_active = 1
    plan.insert(ignore_permissions=True)

    return plan.name


def execute():
    # 1. Membership Plans
    create_plan(
        "Demo Monthly", "GYM-PLAN-MONTHLY",
        "Months", 1, 500, 5
    )

    create_plan(
        "Demo Quarterly", "GYM-PLAN-QUARTERLY",
        "Months", 3, 1300, 10
    )

    create_plan(
        "Demo Class Pack", "GYM-PLAN-CLASS-PACK",
        "Class Pack", 10, 800, 0,
        classes_included=10
    )

    # 2. Gym Rooms
    room_a = get_or_create(
        "Gym Room",
        {"room_name": "Demo Studio A"},
        {"room_name": "Demo Studio A", "capacity": 2, "is_active": 1}
    )

    room_b = get_or_create(
        "Gym Room",
        {"room_name": "Demo Studio B"},
        {"room_name": "Demo Studio B", "capacity": 2, "is_active": 1}
    )

    # 3. Employees and Trainers
    company = frappe.defaults.get_user_default("Company")
    if not company:
        company = frappe.db.get_value("Company", {}, "name")

    gender = frappe.db.get_value("Gender", {}, "name")

    if not company:
        frappe.throw("Create a Company before running seed_data.")

    if not gender:
        frappe.throw("Create a Gender record before running seed_data.")

    trainer_specs = [
        ("Demo Trainer One", "Demo Employee One"),
        ("Demo Trainer Two", "Demo Employee Two"),
    ]

    trainers = []

    for trainer_name, employee_first_name in trainer_specs:
        employee = frappe.db.get_value(
            "Employee", {"first_name": employee_first_name}, "name"
        )

        if not employee:
            emp = frappe.new_doc("Employee")
            emp.first_name = employee_first_name
            emp.gender = gender
            emp.date_of_birth = "1995-01-01"
            emp.date_of_joining = today()
            emp.status = "Active"
            emp.company = company
            emp.insert(ignore_permissions=True)
            employee = emp.name

        trainer = get_or_create(
            "Gym Trainer",
            {"trainer_name": trainer_name},
            {
                "trainer_name": trainer_name,
                "employee": employee,
                "is_active": 1,
            }
        )
        trainers.append(trainer)

    # 4. Gym Classes
    class_specs = [
        {
            "class_name": "Demo Yoga",
            "category": "Yoga",
            "trainer": trainers[0],
            "room": room_a,
            "duration": 60,
            "capacity": 15,
        },
        {
            "class_name": "Demo HIIT",
            "category": "HIIT",
            "trainer": trainers[1],
            "room": room_b,
            "duration": 45,
            "capacity": 12,
        },
    ]

    classes = []

    for data in class_specs:
        class_name = get_or_create(
            "Gym Class",
            {"class_name": data["class_name"]},
            {
                "class_name": data["class_name"],
                "category": data["category"],
                "default_trainer": data["trainer"],
                "default_room": data["room"],
                "duration_minutes": data["duration"],
                "default_capacity": data["capacity"],
            }
        )
        classes.append(class_name)

    # 5. Gym Members
    member_specs = [
        ("Demo Member One", "demo.member1@example.com", "1998-05-12"),
        ("Demo Member Two", "demo.member2@example.com", "2000-08-20"),
        ("Demo Member Three", "demo.member3@example.com", "1997-03-15"),
    ]

    members = []

    for member_name, email, dob in member_specs:
        member = get_or_create(
            "Gym Member",
            {"member_name": member_name},
            {
                "member_name": member_name,
                "email": email,
                "date_of_birth": dob,
                "status": "Active",
            }
        )
        members.append(member)

    # 6. Class Sessions on different days to avoid overlap
    for index, class_name in enumerate(classes):
        session_date = add_days(today(), index + 1)

        existing = frappe.db.exists(
            "Class Session",
            {
                "gym_class": class_name,
                "session_date": session_date,
                "start_time": "09:00:00",
            }
        )

        if not existing:
            gym_class = frappe.get_doc("Gym Class", class_name)

            session = frappe.new_doc("Class Session")
            session.gym_class = class_name
            session.trainer = gym_class.default_trainer
            session.room = gym_class.default_room
            session.session_date = session_date
            session.start_time = "09:00:00"
            session.capacity = gym_class.default_capacity
            session.booked_count = 0
            session.status = "Scheduled"
            session.insert(ignore_permissions=True)

    frappe.db.commit()
    print("Gym Management seed data created successfully.")
