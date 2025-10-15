import React, { useState } from 'react'
import { changePassword } from '../services/api'
import './ChangePassword.css'

export default function ChangePassword({ onSuccess, onCancel }) {
  const [formData, setFormData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  })
  const [showPasswords, setShowPasswords] = useState({
    current: false,
    new: false,
    confirm: false
  })
  const [message, setMessage] = useState({ type: '', text: '' })
  const [loading, setLoading] = useState(false)
  const [validationErrors, setValidationErrors] = useState({})

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    // Clear validation error for this field when user types
    if (validationErrors[name]) {
      setValidationErrors(prev => ({ ...prev, [name]: '' }))
    }
  }

  const togglePasswordVisibility = (field) => {
    setShowPasswords(prev => ({ ...prev, [field]: !prev[field] }))
  }

  const validateForm = () => {
    const errors = {}

    if (!formData.currentPassword) {
      errors.currentPassword = 'Current password is required'
    }

    if (!formData.newPassword) {
      errors.newPassword = 'New password is required'
    } else if (formData.newPassword.length < 6) {
      errors.newPassword = 'Password must be at least 6 characters'
    } else if (formData.newPassword === formData.currentPassword) {
      errors.newPassword = 'New password must be different from current password'
    }

    if (!formData.confirmPassword) {
      errors.confirmPassword = 'Please confirm your new password'
    } else if (formData.newPassword !== formData.confirmPassword) {
      errors.confirmPassword = 'Passwords do not match'
    }

    setValidationErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setMessage({ type: '', text: '' })

    if (!validateForm()) {
      setMessage({ type: 'error', text: 'Please fix the errors below' })
      return
    }

    setLoading(true)

    try {
      // Call the API to change password
      const result = await changePassword(formData.currentPassword, formData.newPassword)
      
      setMessage({ type: 'success', text: result.message || 'Password changed successfully!' })
      setFormData({ currentPassword: '', newPassword: '', confirmPassword: '' })
      
      if (onSuccess) {
        setTimeout(() => onSuccess(), 2000)
      }
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: error.message || 'Failed to change password. Please try again.' 
      })
    } finally {
      setLoading(false)
    }
  }

  const handleCancel = () => {
    setFormData({ currentPassword: '', newPassword: '', confirmPassword: '' })
    setValidationErrors({})
    setMessage({ type: '', text: '' })
    if (onCancel) onCancel()
  }

  return (
    <div className="change-password-container">
      <div className="change-password-header">
        <h2>Change Password</h2>
        <p>Update your password to keep your account secure</p>
      </div>

      <form className="change-password-form" onSubmit={handleSubmit}>
        {message.text && (
          <div className={`cp-message ${message.type}`}>
            {message.type === 'success' ? '✓' : '⚠'} {message.text}
          </div>
        )}

        {/* Current Password */}
        <div className="cp-form-group">
          <label htmlFor="currentPassword">Current Password</label>
          <div className="cp-password-wrapper">
            <input
              type={showPasswords.current ? 'text' : 'password'}
              id="currentPassword"
              name="currentPassword"
              value={formData.currentPassword}
              onChange={handleChange}
              placeholder="Enter your current password"
              disabled={loading}
              className={validationErrors.currentPassword ? 'error' : ''}
            />
            <button
              type="button"
              className="cp-toggle-btn"
              onClick={() => togglePasswordVisibility('current')}
              tabIndex="-1"
            >
              {showPasswords.current ? (
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
                  <line x1="1" y1="1" x2="23" y2="23" />
                </svg>
              ) : (
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                  <circle cx="12" cy="12" r="3" />
                </svg>
              )}
            </button>
          </div>
          {validationErrors.currentPassword && (
            <span className="cp-error-text">{validationErrors.currentPassword}</span>
          )}
        </div>

        {/* New Password */}
        <div className="cp-form-group">
          <label htmlFor="newPassword">New Password</label>
          <div className="cp-password-wrapper">
            <input
              type={showPasswords.new ? 'text' : 'password'}
              id="newPassword"
              name="newPassword"
              value={formData.newPassword}
              onChange={handleChange}
              placeholder="Enter your new password"
              disabled={loading}
              className={validationErrors.newPassword ? 'error' : ''}
            />
            <button
              type="button"
              className="cp-toggle-btn"
              onClick={() => togglePasswordVisibility('new')}
              tabIndex="-1"
            >
              {showPasswords.new ? (
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
                  <line x1="1" y1="1" x2="23" y2="23" />
                </svg>
              ) : (
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                  <circle cx="12" cy="12" r="3" />
                </svg>
              )}
            </button>
          </div>
          {validationErrors.newPassword && (
            <span className="cp-error-text">{validationErrors.newPassword}</span>
          )}
          <span className="cp-hint">Must be at least 6 characters</span>
        </div>

        {/* Confirm Password */}
        <div className="cp-form-group">
          <label htmlFor="confirmPassword">Confirm New Password</label>
          <div className="cp-password-wrapper">
            <input
              type={showPasswords.confirm ? 'text' : 'password'}
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              placeholder="Confirm your new password"
              disabled={loading}
              className={validationErrors.confirmPassword ? 'error' : ''}
            />
            <button
              type="button"
              className="cp-toggle-btn"
              onClick={() => togglePasswordVisibility('confirm')}
              tabIndex="-1"
            >
              {showPasswords.confirm ? (
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
                  <line x1="1" y1="1" x2="23" y2="23" />
                </svg>
              ) : (
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                  <circle cx="12" cy="12" r="3" />
                </svg>
              )}
            </button>
          </div>
          {validationErrors.confirmPassword && (
            <span className="cp-error-text">{validationErrors.confirmPassword}</span>
          )}
        </div>

        {/* Action Buttons */}
        <div className="cp-actions">
          <button
            type="button"
            className="cp-btn secondary"
            onClick={handleCancel}
            disabled={loading}
          >
            Cancel
          </button>
          <button
            type="submit"
            className="cp-btn primary"
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="cp-spinner"></span>
                Changing Password...
              </>
            ) : (
              'Change Password'
            )}
          </button>
        </div>
      </form>
    </div>
  )
}
