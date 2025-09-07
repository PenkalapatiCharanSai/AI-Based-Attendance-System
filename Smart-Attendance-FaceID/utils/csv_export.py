import csv
import os
from models.user_model import get_all_attendance, get_attendance_by_date

# =============== CSV EXPORT UTILS ===============

def export_attendance_all(filename="attendance_all.csv"):
    """
    Export all attendance records to a CSV file.
    """
    records = get_all_attendance()
    if not records:
        return False, "No attendance records found."

    fieldnames = ["student_id", "name", "year", "department", "date", "time", "status"]

    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    return True, f"All attendance exported to {os.path.abspath(filename)}"


def export_attendance_by_date(date_str, filename=None):
    """
    Export attendance records for a specific date to a CSV file.
    """
    records = get_attendance_by_date(date_str)
    if not records:
        return False, f"No attendance records found for {date_str}."

    if filename is None:
        filename = f"attendance_{date_str}.csv"

    fieldnames = ["student_id", "name", "year", "department", "date", "time", "status"]

    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    return True, f"Attendance for {date_str} exported to {os.path.abspath(filename)}"
