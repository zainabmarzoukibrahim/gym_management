# Copyright (c) 2026, zainab@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime, add_to_date, get_time


class ClassSession(Document):
    def validate(self):
        if self.gym_class:
            gym_class = frappe.get_doc("Gym Class", self.gym_class)

            if not self.trainer:
                self.trainer = gym_class.default_trainer

            if self.start_time and gym_class.duration_minutes:
                start_datetime = get_datetime(
                    f"{self.session_date} {self.start_time}"
                )
                end_datetime = add_to_date(
                    start_datetime,
                    minutes=gym_class.duration_minutes
                )
                self.end_time = end_datetime.strftime("%H:%M:%S")

        if self.trainer and self.room and self.session_date:
            self.check_overlapping_sessions()

    def check_overlapping_sessions(self):
        if not self.start_time or not self.end_time:
            return

        filters = {
            "session_date": self.session_date,
            "status": ["!=", "Cancelled"],
            "name": ["!=", self.name or ""],
        }

        sessions = frappe.get_all(
            "Class Session",
            filters=filters,
            fields=["name", "trainer", "room", "start_time", "end_time"]
        )

        new_start = get_time(self.start_time)
        new_end = get_time(self.end_time)

        for session in sessions:
            session_start = get_time(session.start_time)
            session_end = get_time(session.end_time)

            overlaps = (
                new_start < session_end
                and new_end > session_start
            )

            if not overlaps:
                continue

            if self.trainer == session.trainer:
                frappe.throw(
                    f"Trainer already has an overlapping session: {session.name}"
                )

            if self.room == session.room:
                frappe.throw(
                    f"Room already has an overlapping session: {session.name}"
                )
