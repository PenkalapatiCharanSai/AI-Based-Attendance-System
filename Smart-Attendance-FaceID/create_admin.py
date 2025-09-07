from utils.auth_utils import create_admin

# Change username/password as needed
success, msg = create_admin("admin", "admin123")
print(msg)
