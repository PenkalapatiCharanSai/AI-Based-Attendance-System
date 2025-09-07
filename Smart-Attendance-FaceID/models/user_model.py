from pymongo import MongoClient
from config import Config
import datetime

# Initialize MongoDB connection
client = MongoClient(Config.MONGO_URI)
db = client[Config.DB_NAME]

users_col = db[Config.USERS_COLLECTION]
attendance_col = db[Config.ATTENDANCE_COLLECTION]

# =============== USER FUNCTIONS ===============

def register_user(student_id, name, year, department, face_encoding):
    """
    Register a new student with face encoding.
    """
    user_data = {
        "student_id": student_id,
        "name": name,
        "year": year,                   # Added Year
        "department": department,
        "face_encoding": face_encoding.tolist(),  # numpy array → list
        "created_at": datetime.datetime.now()
    }

    # Prevent duplicate student_id
    if users_col.find_one({"student_id": student_id}):
        return False, "Student already registered."

    users_col.insert_one(user_data)
    return True, "Student registered successfully."


def get_all_users():
    """
    Fetch all registered students.
    """
    return list(users_col.find({}, {"_id": 0, "face_encoding": 0}))


def get_user_by_id(student_id):
    """
    Fetch single student by ID.
    """
    return users_col.find_one({"student_id": student_id}, {"_id": 0})


def get_all_face_encodings():
    """
    Return list of all face encodings with student IDs.
    """
    users = list(users_col.find({}, {"student_id": 1, "name": 1, "face_encoding": 1, "_id": 0}))
    return users


# =============== ATTENDANCE FUNCTIONS ===============

def mark_attendance(student_id, status="Present"):
    """
    Mark attendance for a student.
    """
    student = get_user_by_id(student_id)
    if not student:
        return False, "Student not found."

    log = {
        "student_id": student["student_id"],
        "name": student["name"],
        "year": student["year"],
        "department": student["department"],
        "date": datetime.date.today().strftime("%Y-%m-%d"),
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "status": status
    }

    # Prevent duplicate entry for same day
    existing = attendance_col.find_one({
        "student_id": student_id,
        "date": log["date"]
    })

    if existing:
        return False, "Attendance already marked."

    attendance_col.insert_one(log)
    return True, "Attendance marked."


def get_attendance_by_date(date_str):
    """
    Fetch attendance records for a specific date.
    """
    return list(attendance_col.find({"date": date_str}, {"_id": 0}))


def get_all_attendance():
    """
    Fetch all attendance records.
    """
    return list(attendance_col.find({}, {"_id": 0}))
