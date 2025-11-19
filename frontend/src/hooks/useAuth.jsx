import React, { createContext, useContext, useEffect, useState } from 'react'
import { onAuthStateChanged, signInWithEmailAndPassword, signOut, updatePassword } from 'firebase/auth'
import { doc, getDoc } from 'firebase/firestore'
import { verifyToken } from '../services/api'

import { auth, db } from '../firebase'

const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [userRole, setUserRole] = useState(null)
  const [userEpf, setUserEpf] = useState(null) // Store EPF for the logged-in user
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (u) => {
      setUser(u)
      if (u) {
        try {
          // Get fresh token (force refresh to avoid expired tokens)
          const idToken = await u.getIdToken(true)
          try {
            const payload = await verifyToken(idToken)
            setUserRole(payload.role || 'user')
            setUserEpf(payload.epf || null)
          } catch (err) {
            console.warn('Backend verify failed, falling back to Firestore lookup', err)
            
            // Lookup user by UID (users are now stored by UID)
            const docRef = doc(db, 'users', u.uid)
            const snap = await getDoc(docRef)
            if (snap.exists()) {
              const userData = snap.data()
              setUserRole(userData.role || 'user')
              setUserEpf(userData.epf || null)
            } else {
              setUserRole('user')
            }
          }
        } catch (err) {
          console.error('Failed to get user role or token', err)
          setUserRole('user')
        }
      } else {
        // User logged out - clear all state and sessionStorage
        setUserRole(null)
        setUserEpf(null)
        sessionStorage.clear()
      }
      setLoading(false)
    })
    return unsubscribe
  }, [])

  const login = async (epf, password) => {
    // Look up EPF in Firestore users collection to get the email
    try {
      const userDoc = await getDoc(doc(db, 'users', epf))
      if (!userDoc.exists()) {
        throw new Error(`EPF number ${epf} not found. Please contact administrator.`)
      }
      
      const userData = userDoc.data()
      
      // Check if email field exists in the document
      let email = userData.email
      
      // If no email field, construct email from EPF (fallback)
      if (!email) {
        email = `${epf}@ou.ac.lk`
      }
      
      // Store EPF in session storage for later role lookup
      sessionStorage.setItem('userEpf', epf)
      
      // Sign in with email and password
      const userCredential = await signInWithEmailAndPassword(auth, email, password)
      
      // Get fresh token immediately after login
      const idToken = await userCredential.user.getIdToken(true)
      
      // Verify token with backend
      try {
        const payload = await verifyToken(idToken)
        setUserRole(payload.role || 'user')
        setUserEpf(payload.epf || epf)
      } catch (err) {
        console.warn('Token verification failed after login:', err)
      }
      
      return userCredential
    } catch (err) {
      console.error('EPF login failed:', err)
      throw err
    }
  }

  const logout = async () => {
    // Clear agent token file
    try {
      await fetch('http://localhost:8000/print/clear-agent-token', {
        method: 'POST'
      })
      console.log('✅ Agent token cleared')
    } catch (err) {
      console.error('Failed to clear agent token:', err)
      // Don't block logout if this fails
    }
    
    // Clear sessionStorage to prevent role persistence across logins
    sessionStorage.removeItem('userEpf')
    sessionStorage.clear()
    return signOut(auth)
  }

  const changePassword = (newPassword) => {
    if (!auth.currentUser) return Promise.reject(new Error('No user'))
    return updatePassword(auth.currentUser, newPassword)
  }

  return (
    <AuthContext.Provider value={{ user, userRole, userEpf, loading, login, logout, changePassword }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
