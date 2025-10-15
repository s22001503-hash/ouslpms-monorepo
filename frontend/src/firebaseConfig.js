// Firebase config read from Vite environment variables with sensible fallbacks
// (the fallback values were provided by the user)
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || 'AIzaSyBw98pSudMcx_4T6Y-_ICTveOcFfqSKZz0',
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || 'oct-project-25fad.firebaseapp.com',
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || 'oct-project-25fad',
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || 'oct-project-25fad.firebasestorage.app',
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || '105648964923',
  appId: import.meta.env.VITE_FIREBASE_APP_ID || '1:105648964923:web:7b940d9d24cc0a5d91231e',
  measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID || 'G-Z6K43WLJLH',
}

export default firebaseConfig
