import os

class Config:
    # Secret key for Flask session handling
    SECRET_KEY = os.environ.get("SECRET_KEY") or "mysecretkey"

    # MongoDB connection
    MONGO_URI = os.environ.get("MONGO_URI") or "mongodb+srv://charan:charan@cluster0.zmg8d.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # Database & Collection names
    DB_NAME = "attendance_db"
    USERS_COLLECTION = "users"
    ATTENDANCE_COLLECTION = "attendance"
