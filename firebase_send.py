import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def find_user_license_plate(plate_num: str) -> str:
    # returns a user id given a license plate number
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    users_ref = db.collection(u'users')
    docs = users_ref.stream()
    for doc in docs:
        data = doc.to_dict()
        if data["license_plate"] == plate_num:
            return data["user_id"]
    return None

def send_push_notification(plate_num: str):
    user_id = find_user_license_plate(plate_num)
    if user_id is None:
        return "User not found"
    # send push notification to user
    return "Push notification sent to user with id: " + user_id