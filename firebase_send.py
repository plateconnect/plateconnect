import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def find_user_license_plate(plate_num: str) -> str:
    # returns ward ids given a license plate number
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    users_ref = db.collection(u'users')
    docs = users_ref.stream()
    for doc in docs:
        data = doc.to_dict()
        license_plates = data["license_plates"]

        for plate in license_plates:
            if plate == plate_num:
                ward_ids = data["ward_ids"]

                for _id in ward_ids:
                    print(get_student_name(_id))
                    pass
    return None


def get_student_name(ward_id: str) -> str:
    # returns student names given a ward id
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    users_ref = db.collection(u'users')
    docs = users_ref.stream()
    for doc in docs:
        data = doc.to_dict()
        ward_ids = data["ward_ids"]
        for _id in ward_ids:
            if _id == ward_id:
                return data["name"]
    return None

def send_push_notification(plate_num: str):
    user_id = find_user_license_plate(plate_num)
    if user_id is None:
        return "User not found"
    # send push notification to user
    return "Push notification sent to user with id: " + user_id