from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, admin, dean, print as print_router, ai
import firebase_admin
from firebase_admin import credentials
import os
import logging
import openai  # ✅ NEW: For executive summary generation
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    try:
        # Check if running in production (Cloud Run) or local
        if os.getenv('GOOGLE_CLOUD_PROJECT'):
            # Production: Use default credentials
            firebase_admin.initialize_app()
            logger.info("✅ Firebase Admin initialized with default credentials")
        else:
            # Local: Use service account key
            cred_path = os.path.join(os.path.dirname(__file__), '..', 'serviceAccountKey.json')
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                logger.info("✅ Firebase Admin initialized with service account key")
            else:
                # Fallback: Initialize without credentials (Firestore will fail but API will work)
                logger.warning("⚠️ No Firebase credentials found - Firestore features will be disabled")
                logger.warning("⚠️ To enable Firestore, download serviceAccountKey.json from Firebase Console")
                # Don't initialize Firebase at all if no credentials
                # firebase_admin.initialize_app()
    except Exception as e:
        logger.error(f"❌ Firebase Admin initialization failed: {e}")
        logger.warning("⚠️ Continuing without Firebase - some features may not work")

# ✅ NEW: Initialize OpenAI API
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    openai.api_key = openai_api_key
    logger.info("✅ OpenAI API initialized for executive summary generation")
else:
    logger.warning("⚠️ OPENAI_API_KEY not found - executive summary generation will fail")
    logger.warning("⚠️ Set OPENAI_API_KEY environment variable to enable this feature")

app = FastAPI(title='OUSPMS Backend')

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5177",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5177",
        "http://localhost:8000",  # Allow virtual printer agent
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(auth.router, prefix='/auth')
app.include_router(admin.router, prefix='/admin')
app.include_router(dean.router, prefix='/dean')
app.include_router(print_router.router, prefix='/print')
app.include_router(ai.router, prefix='/ai')

@app.get('/')
def root():
    return {'status': 'ok'}
