Backend FastAPI service for OUSPMS

Environment:
- Set `GOOGLE_APPLICATION_CREDENTIALS` to your service account JSON file path, or set `FIREBASE_SERVICE_ACCOUNT` env var to the JSON content.

Run:
- python -m pip install -r requirements.txt
- uvicorn app.main:app --reload --port 8000
