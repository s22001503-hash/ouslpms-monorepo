import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { auth } from '../firebase'
import { signInWithEmailAndPassword } from 'firebase/auth'
import './LoginPage.css'

export default function LoginPage() {
  const [epf, setEpf] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const { login, userRole } = useAuth()
  const navigate = useNavigate()

  const [loadingRedirect, setLoadingRedirect] = React.useState(false)

  const handleLoginAsUser = async (e) => {
    e.preventDefault()
    setError(null)
    setIsLoading(true)
    
    try {
      await login(epf, password)
      setLoadingRedirect(true)
    } catch (err) {
      setError(err.message || 'Login failed. Please check your credentials.')
      setIsLoading(false)
    }
  }

  const handleLoginAsAdmin = async (e) => {
    e.preventDefault()
    setError(null)
    setIsLoading(true)
    
    try {
      await login(epf, password)
      setLoadingRedirect(true)
    } catch (err) {
      setError(err.message || 'Login failed. Please check your credentials.')
      setIsLoading(false)
    }
  }

  // when loadingRedirect becomes true, wait for userRole to populate
  React.useEffect(() => {
    if (loadingRedirect) {
      if (userRole) {
        if (userRole === 'admin') navigate('/admin')
        else navigate('/user')
      } else {
        // If role still null after some time, fallback to /user
        const t = setTimeout(() => {
          navigate('/user')
        }, 2000)
        return () => clearTimeout(t)
      }
    }
  }, [loadingRedirect, userRole, navigate])

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

  <form className="login-form" autoComplete="off">
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
              disabled={isLoading}
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
                disabled={isLoading}
              />
              <button
                type="button"
                className="show-password-btn"
                onClick={() => setShowPassword((s) => !s)}
                aria-label={showPassword ? 'Hide password' : 'Show password'}
                title={showPassword ? 'Hide password' : 'Show password'}
              >
                {showPassword ? (
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 3l18 18" stroke="#2d3748" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M10.58 10.58A3 3 0 0 0 13.42 13.42" stroke="#2d3748" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M12 5c5 0 9 4 9 7s-4 7-9 7c-1.27 0-2.47-.22-3.57-.62" stroke="#2d3748" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                ) : (
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12z" stroke="#2d3748" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <circle cx="12" cy="12" r="3" stroke="#2d3748" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                )}
              </button>
            </div>
          </div>

          {error && (
            <div className="error-message">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18Z" stroke="currentColor" strokeWidth="2"/>
                <path d="M10 6V10M10 14H10.01" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              </svg>
              <span>{error}</span>
            </div>
          )}

          <button 
            type="submit" 
            onClick={handleLoginAsUser}
            className="login-button primary" 
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <span className="spinner"></span>
                Logging in...
              </>
            ) : (
              'Login as User'
            )}
          </button>

          <button 
            type="button"
            onClick={handleLoginAsAdmin}
            className="login-button secondary" 
            disabled={isLoading}
          >
            Login as Admin
          </button>
        </form>
      </div>
    </div>
  )
}
