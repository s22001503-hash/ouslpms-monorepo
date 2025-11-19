# Google Drive Setup Instructions

## Step-by-Step Guide to Enable Google Drive Integration

### Step 1: Access Google Cloud Console

1. Go to https://console.cloud.google.com
2. Sign in with your Google account (use `lahirujee123@gmail.com`)

### Step 2: Select or Create Project

1. At the top of the page, click the project dropdown
2. Select your existing project: **oct-project-25fad**
   - If not created yet, click "New Project"
   - Name it `oct-project-25fad`
   - Click "Create"

### Step 3: Enable Google Drive API

1. In the left sidebar, click **APIs & Services** → **Library**
2. In the search box, type: `Google Drive API`
3. Click on "Google Drive API"
4. Click the **Enable** button
5. Wait for it to enable (takes a few seconds)

### Step 4: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **+ Create Credentials** at the top
3. Select **OAuth client ID**

4. **Configure OAuth Consent Screen** (if not done yet):
   - Click "Configure Consent Screen"
   - User Type: **External** (unless you have Google Workspace)
   - Click "Create"
   
   **App Information:**
   - App name: `EcoPrint`
   - User support email: `lahirujee123@gmail.com`
   - Developer contact: `lahirujee123@gmail.com`
   - Click "Save and Continue"
   
   **Scopes:**
   - Click "Add or Remove Scopes"
   - Search for: `.../auth/drive.file`
   - Check the box for "See, edit, create, and delete only the specific Google Drive files you use with this app"
   - Click "Update"
   - Click "Save and Continue"
   
   **Test Users** (for development):
   - Click "Add Users"
   - Add your email: `lahirujee123@gmail.com`
   - Click "Save and Continue"
   - Click "Back to Dashboard"

5. **Create OAuth Client ID:**
   - Go back to **Credentials** → **Create Credentials** → **OAuth client ID**
   - Application type: **Web application**
   - Name: `EcoPrint Web Client`
   
   **Authorized JavaScript origins:**
   - Click "Add URI"
   - Add: `http://localhost:5174`
   - Click "Add URI" again
   - Add: `http://localhost:5173` (backup)
   
   **Authorized redirect URIs:**
   - Click "Add URI"
   - Add: `http://localhost:5174/oauth2callback`
   - Click "Add URI"
   - Add: `http://localhost:5173/oauth2callback`
   
   - Click **Create**

6. **Save Your Credentials:**
   - A popup will show your credentials
   - Copy the **Client ID** (looks like: `xxx.apps.googleusercontent.com`)
   - Copy the **Client Secret**
   - Click "OK"

### Step 5: Create API Key

1. Still in **Credentials**, click **+ Create Credentials**
2. Select **API Key**
3. Copy the API Key that appears
4. Click "Edit API Key" (or the pencil icon)
5. Under "API restrictions":
   - Select "Restrict key"
   - Check "Google Drive API"
   - Click "Save"

### Step 6: Configure Environment Variables

1. Open your project folder: `C:\Users\user\Desktop\OCT project\ouslpms-monorepo\frontend`

2. Create a file named `.env` (if it doesn't exist)

3. Add these lines (replace with your actual credentials):

```env
VITE_GOOGLE_CLIENT_ID=YOUR_CLIENT_ID_HERE.apps.googleusercontent.com
VITE_GOOGLE_API_KEY=YOUR_API_KEY_HERE
```

**Example:**
```env
VITE_GOOGLE_CLIENT_ID=123456789-abc123def456.apps.googleusercontent.com
VITE_GOOGLE_API_KEY=AIzaSyABCDEFGHIJKLMNOPQRSTUVWXYZ
```

4. Save the file

### Step 7: Install Required Package

Open PowerShell in the frontend directory and run:

```powershell
cd "C:\Users\user\Desktop\OCT project\ouslpms-monorepo\frontend"
npm install gapi-script
```

### Step 8: Restart Development Server

1. Stop the current dev server (Ctrl+C in terminal)
2. Restart it:
```powershell
npm run dev
```

### Step 9: Test the Integration

1. Go to http://localhost:5174
2. Login as a user
3. Go to "Print Document"
4. Upload a document
5. When classification completes, click "Confirm & Print"
6. In the confirmation dialog, click "💾 Save to Google Drive"
7. You should see:
   - Google sign-in popup
   - Permission request
   - Upload progress
   - Success message with Drive link

## Troubleshooting

### Error: "Access blocked: Authorization Error"
- Go back to OAuth consent screen
- Make sure your email is added as a Test User
- Status should be "Testing" (not "Published")

### Error: "Invalid client"
- Check that Client ID in `.env` matches Google Console
- Make sure you're using `VITE_` prefix for environment variables
- Restart dev server after changing `.env`

### Error: "redirect_uri_mismatch"
- Make sure `http://localhost:5174` is in Authorized JavaScript origins
- Check for typos in the URL
- No trailing slashes

### Google popup blocked
- Allow popups for localhost in your browser
- Try again

## Security Notes

- **Never commit `.env` file to git** (it's already in `.gitignore`)
- For production, add your production domain to authorized origins
- Keep Client Secret secure (only needed for backend integration)

## Next Steps After Setup

Once credentials are configured:
1. Test upload to Drive
2. Verify files appear in user's Drive
3. Check that Drive links work
4. Test with different file types

## Support

If you encounter issues:
1. Check browser console for errors (F12)
2. Verify credentials in Google Cloud Console
3. Make sure APIs are enabled
4. Check that `.env` file is in the correct location
