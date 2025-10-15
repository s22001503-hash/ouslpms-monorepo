import { initializeApp, getApps } from 'firebase/app'
import { getAnalytics } from 'firebase/analytics'
import { getAuth } from 'firebase/auth'
import { getFirestore } from 'firebase/firestore'
import firebaseConfig from './firebaseConfig'

// Initialize or reuse existing app (prevents duplicate initialization errors)
const app = !getApps().length ? initializeApp(firebaseConfig) : getApps()[0]

let analytics = null
try {
  // Analytics is browser-only and may throw in non-browser envs; guard it
  if (typeof window !== 'undefined' && firebaseConfig.measurementId) {
    analytics = getAnalytics(app)
  }
} catch (err) {
  // Analytics may not be available in some environments; swallow safely
  // eslint-disable-next-line no-console
  console.warn('Firebase analytics not initialized:', err && err.message ? err.message : err)
}

const auth = getAuth(app)
const db = getFirestore(app)

export { app, analytics, auth, db }
