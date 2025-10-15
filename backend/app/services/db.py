from firebase_admin import firestore

# Simple wrapper for Firestore access

def get_user_role(uid: str) -> str:
    db = firestore.client()
    doc_ref = db.collection('users').document(uid)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get('role', 'user')
    return 'user'
