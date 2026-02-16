import json
import os

USER_FILE = r"model\user.json"


def save_username(username):
    """שומר את שם המשתמש לקובץ JSON (מעדכן רק את username)"""
    data = _load_user_data()
    data["username"] = username
    _save_user_data(data)


def load_username():
    """טוען את שם המשתמש מהקובץ"""
    data = _load_user_data()
    return data.get("username")


def save_user_id(user_id):
    """שומר את userID לקובץ JSON (מעדכן רק את userID)"""
    data = _load_user_data()
    data["userID"] = user_id
    _save_user_data(data)


def load_user_id():
    """טוען את userID מהקובץ"""
    data = _load_user_data()
    return data.get("userID")


# --- פונקציות עזר פרטיות ---

def _load_user_data():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # מחזיר מילון ריק אם אין קובץ או מבנה פגום


def _save_user_data(data):
    os.makedirs(os.path.dirname(USER_FILE), exist_ok=True)
    with open(USER_FILE, "w") as f:
        json.dump(data, f, indent=4)


# --- בדיקה ---
if __name__ == "__main__":
    save_username("shneor")
    save_user_id(4)
    print("Loaded username:", load_username())
    print("Loaded userID:", load_user_id())
