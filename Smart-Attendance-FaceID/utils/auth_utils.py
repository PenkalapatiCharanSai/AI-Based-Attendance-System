from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from config import Config

# Connect to DB
client = MongoClient(Config.MONGO_URI)
db = client[Config.DB_NAME]
admin_col = db["admins"]

# =============== AUTH UTILS ===============

def create_admin(username, password):
    """
    Create a new admin account (only once or for setup).
    """
    if admin_col.find_one({"username": username}):
        return False, "Admin already exists."

    hashed_pw = generate_password_hash(password)
    admin_col.insert_one({"username": username, "password": hashed_pw})
    return True, "Admin account created."


def verify_admin(username, password):
    """
    Verify login credentials for admin.
    """
    admin = admin_col.find_one({"username": username})
    if not admin:
        return False, "Admin not found."

    if check_password_hash(admin["password"], password):
        return True, "Login successful."
    else:
        return False, "Invalid password."
