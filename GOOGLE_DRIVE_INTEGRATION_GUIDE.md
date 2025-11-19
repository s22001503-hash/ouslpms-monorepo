# Google Drive Integration Guide

## Overview
Integrate Google Drive API to save documents directly to user's Drive instead of printing.

## Implementation Steps

### 1. Enable Google Drive API

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project: `oct-project-25fad`
3. Enable APIs:
   - Go to "APIs & Services" → "Library"
   - Search for "Google Drive API"
   - Click "Enable"

### 2. Configure OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client ID"
3. Application type: "Web application"
4. Name: "EcoPrint Drive Integration"
5. Authorized JavaScript origins:
   - `http://localhost:5174` (development)
   - `https://your-production-domain.com` (production)
6. Authorized redirect URIs:
   - `http://localhost:5174/auth/google/callback`
   - `https://your-production-domain.com/auth/google/callback`
7. Click "Create" and save:
   - **Client ID**
   - **Client Secret**

### 3. Install Dependencies

#### Frontend:
```bash
cd frontend
npm install @react-oauth/google gapi-script
```

#### Backend (Optional - for server-side upload):
```bash
cd backend
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 4. Environment Variables

Create `.env` files:

#### Frontend `.env`:
```env
VITE_GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
VITE_GOOGLE_API_KEY=your-api-key-here
```

#### Backend `.env`:
```env
GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret-here
```

## Implementation Options

### Option A: Frontend-Only (Recommended for Simple Use)

**Pros:**
- No backend changes needed
- Direct upload from browser
- Faster implementation

**Cons:**
- Requires user to grant Drive permissions each time
- Limited server-side tracking

### Option B: Backend-Mediated (Better for Production)

**Pros:**
- Server tracks all saved documents
- Can attach to user's print history
- Better security and audit trail

**Cons:**
- More complex implementation
- Requires file upload to backend first

## Frontend Implementation (Option A)

I'll create the necessary files for frontend Google Drive integration.

### Files to Create:
1. `frontend/src/services/googleDrive.js` - Drive API wrapper
2. `frontend/src/components/GoogleDriveButton.jsx` - Reusable Drive button
3. Update `PrintConfirmationDialog.jsx` to use Drive integration

### How It Works:
1. User clicks "Save to Google Drive"
2. Google OAuth popup appears (one-time permission)
3. User grants Drive access
4. Document uploads to user's Drive
5. Success message with Drive link
6. No print quota used

## Next Steps:
1. Get OAuth credentials from Google Cloud Console
2. Install npm packages
3. I'll create the integration code
4. Test the flow

Would you like me to:
1. Create the frontend Google Drive integration code now?
2. Create the backend-mediated version instead?
3. Wait for you to get the OAuth credentials first?

Let me know your preference!
