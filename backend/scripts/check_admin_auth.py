import os
import firebase_admin
from firebase_admin import credentials, auth

cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
print('GOOGLE_APPLICATION_CREDENTIALS =', cred_path)
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    print('firebase_admin initialized:', bool(firebase_admin._apps))
    try:
        user = auth.get_user_by_email('50005@ousl.edu.lk')
        print('Found user:', user.uid, user.email)
    except Exception as e:
        print('Auth.get_user_by_email error: ', repr(e))
except Exception as e:
    print('Initialization error:', repr(e))
