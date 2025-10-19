import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { signInWithEmailAndPassword, signOut } from 'firebase/auth'
import { doc, getDoc, updateDoc } from 'firebase/firestore'
import { auth, db } from '../firebase'
import './LoginPage.css'

export default function LoginPage() {
  const navigate = useNavigate()
  const [epf, setEpf] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showPassword, setShowPassword] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    if (!epf || !password) {
      setError('Please enter both EPF and password')
      setLoading(false)
      return
    }

    try {
      // Trim whitespace from EPF input
      const cleanEpf = epf.trim()
      const email = `${cleanEpf}@ousl.edu.lk`
      
      console.log('Login attempt:', { epf: cleanEpf, email })
      
      // Clear any previous session data before logging in
      sessionStorage.clear()
      
      // Get user data from Firestore FIRST to verify role exists
      const userDoc = await getDoc(doc(db, 'users', cleanEpf))
      
      if (!userDoc.exists()) {
        setError('User not found. Please contact administrator.')
        setLoading(false)
        return
      }
      
      const userData = userDoc.data()
      const userRole = userData.role

      console.log('=== LOGIN DEBUG ===')
      console.log('EPF:', cleanEpf)
      console.log('User Data:', userData)
      console.log('User Role:', userRole)
      console.log('Role Type:', typeof userRole)

      // Store EPF in sessionStorage BEFORE signing in so useAuth can read it immediately
      sessionStorage.setItem('userEpf', cleanEpf)
      
      // Sign in with Firebase Auth
      const userCredential = await signInWithEmailAndPassword(auth, email, password)
      const user = userCredential.user

      // Update last login timestamp
      await updateDoc(doc(db, 'users', cleanEpf), {
        lastLogin: new Date().toISOString()
      })

      console.log(`User logged in: ${userData.name} (Role: ${userRole})`)

      // Redirect based on role - automatically detect and route
      if (userRole === 'admin') {
        console.log('Navigating to /admin')
        navigate('/admin', { replace: true })
      } else if (userRole === 'dean') {
        console.log('Navigating to /dean')
        navigate('/dean', { replace: true })
      } else if (userRole === 'user') {
        console.log('Navigating to /user')
        navigate('/user', { replace: true })
      } else {
        console.log('Invalid role detected:', userRole)
        setError('Invalid user role. Please contact administrator.')
        await signOut(auth)
      }
    } catch (err) {
      console.error('Login error:', err)
      console.error('Error code:', err.code)
      console.error('Error message:', err.message)
      
      if (err.code === 'auth/user-not-found' || err.code === 'auth/wrong-password') {
        setError('Invalid EPF or password')
      } else if (err.code === 'auth/invalid-credential') {
        setError('Invalid credentials. Please check your EPF and password.')
      } else if (err.code === 'auth/invalid-email') {
        setError(`Invalid email format. Tried: ${epf.trim()}@ousl.edu.lk`)
      } else if (err.code === 'auth/too-many-requests') {
        setError('Too many failed login attempts. Please try again later.')
      } else {
        setError(err.message || 'Login failed. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <div className="logo">
            <img src="/OUSL LOGO.jpg" alt="OUSL Logo" className="logo-image" />
          </div>
          <h1>EcoPrint</h1>
          <p className="subtitle">Smart Print Management System</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form" autoComplete="off">
          {error && (
            <div className="error-message">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18Z" stroke="currentColor" strokeWidth="2"/>
                <path d="M10 6V10M10 14H10.01" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              </svg>
              <span>{error}</span>
            </div>
          )}

          <div className="form-group">
            <label htmlFor="epf">EPF Number</label>
            <input
              id="epf"
              name="epf"
              autoComplete="username"
              type="text"
              value={epf}
              onChange={(e) => setEpf(e.target.value)}
              placeholder="Enter your EPF Number"
              required
              disabled={loading}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <div className="password-wrapper">
              <input
                id="password"
                name="password"
                autoComplete="current-password"
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your Password"
                required
                disabled={loading}
              />
              <button
                type="button"
                className="show-password-btn"
                onClick={() => setShowPassword(!showPassword)}
                aria-label={showPassword ? 'Hide password' : 'Show password'}
                title={showPassword ? 'Hide password' : 'Show password'}
              >
                {showPassword ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
          </div>

          <button 
            type="submit" 
            className="login-button primary" 
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Logging in...
              </>
            ) : (
              'Login'
            )}
          </button>
        </form>
      </div>
    </div>
  )
}
