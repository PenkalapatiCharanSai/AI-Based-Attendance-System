import os

class Config:
    # Secret key for Flask session handling
    SECRET_KEY = os.environ.get("SECRET_KEY") or "mysecretkey"

    # MongoDB connection
    MONGO_URI = os.environ.get("MONGO_URI") or "mongodb://localhost:27017/"

    # Database & Collection names
    DB_NAME = "attendance_db"
    USERS_COLLECTION = "users"
    ATTENDANCE_COLLECTION = "attendance"

