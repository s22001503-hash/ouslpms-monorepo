# OUSPMS Monorepo

Open University Smart Print Management System - Monorepo scaffold for Sprint 1

Structure:

- frontend: React (Vite) app with Firebase Auth integration
- backend: FastAPI service with Firebase Admin token verification

Sprint 1 - Setup & Authentication

This scaffold includes starter code for:
- React + Vite app (minimal)
- Firebase auth hook and services
- LoginPage, ChangePassword, UserDashboard, AdminDashboard components
- React Router wiring
- FastAPI app with `/auth/verify` route that validates Firebase ID tokens

Setup notes

Frontend:
- Install dependencies with npm or yarn inside `frontend/`.
- Create a Firebase project and add config to `frontend/src/firebaseConfig.js`.

Backend:
- Provide a Firebase service account JSON and set environment variable `GOOGLE_APPLICATION_CREDENTIALS` or set `FIREBASE_SERVICE_ACCOUNT` as JSON string.
- Install dependencies from `backend/requirements.txt`.
- Run the backend with `uvicorn app.main:app --reload --port 8000`.

Next steps:
- Implement role-based UI and Firestore rules
- Add document classification AI service (Sprint 2)
