import React, { useState } from 'react'
import './PolicyViolationDialog.css'

/**
 * PolicyViolationDialog - Shows when print request violates policy
 * Displays violation reason and alternative options
 */
export default function PolicyViolationDialog({ 
  isOpen, 
  onRequestPermission,
  onSaveToDrive,
  onCancel,
  fileName,
  violationType, // 'daily_limit' or 'copies_limit'
  violationMessage
}) {
  const [showPermissionForm, setShowPermissionForm] = useState(false)
  const [justification, setJustification] = useState('')

  if (!isOpen) return null

  const handleRequestPermission = () => {
    setShowPermissionForm(true)
  }

  const handleSubmitRequest = () => {
    if (!justification.trim()) {
      alert('Please provide a justification for your request')
      return
    }
    onRequestPermission(justification)
    setJustification('')
    setShowPermissionForm(false)
  }

  return (
    <div className="pvd-overlay">
      <div className="pvd-dialog">
        <div className="pvd-header">
          <h2>⚠️ PRINT POLICY VIOLATION</h2>
        </div>

        <div className="pvd-body">
          {/* Violation Status */}
          <div className="pvd-violation">
            <div className="pvd-violation-icon">🚫</div>
            <div className="pvd-violation-text">
              <strong>Cannot Print: Policy Limit Reached</strong>
              <div className="pvd-filename">{fileName}</div>
            </div>
          </div>

          {/* Violation Reason */}
          <div className="pvd-reason">
            <h3>📋 Reason:</h3>
            <p>{violationMessage}</p>
          </div>

          {!showPermissionForm ? (
            <>
              {/* Alternative Options */}
              <div className="pvd-options">
                <h3>🔄 To proceed, please choose an option:</h3>

                <div className="pvd-option-card">
                  <div className="pvd-option-icon">📧</div>
                  <div className="pvd-option-content">
                    <strong>Share a Digital Copy</strong>
                    <p>Send via Email, WhatsApp, or Telegram</p>
                  </div>
                </div>

                <div className="pvd-option-card">
                  <div className="pvd-option-icon">💾</div>
                  <div className="pvd-option-content">
                    <strong>Save for Later</strong>
                    <p>Store it in Google Drive or OneDrive</p>
                  </div>
                </div>

                <div className="pvd-option-card">
                  <div className="pvd-option-icon">👤</div>
                  <div className="pvd-option-content">
                    <strong>Request Special Permission</strong>
                    <p>Explain why you need to print this</p>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="pvd-actions">
                <button 
                  className="pvd-btn pvd-btn-permission"
                  onClick={handleRequestPermission}
                >
                  👤 Request Permission
                </button>
                <button 
                  className="pvd-btn pvd-btn-drive"
                  onClick={onSaveToDrive}
                >
                  💾 Save to Drive
                </button>
                <button 
                  className="pvd-btn pvd-btn-cancel"
                  onClick={onCancel}
                >
                  ❌ Cancel
                </button>
              </div>
            </>
          ) : (
            <>
              {/* Permission Request Form */}
              <div className="pvd-permission-form">
                <h3>📝 Request Special Permission</h3>
                <p className="pvd-form-hint">
                  Explain why you need to print this document. Your request will be sent to the HOD for approval.
                </p>
                <textarea
                  className="pvd-justification"
                  placeholder="Example: Urgent academic materials needed for tomorrow's lecture. This is essential for teaching and cannot be shared digitally due to classroom requirements..."
                  value={justification}
                  onChange={(e) => setJustification(e.target.value)}
                  rows={5}
                />
                <div className="pvd-form-actions">
                  <button 
                    className="pvd-btn pvd-btn-submit"
                    onClick={handleSubmitRequest}
                  >
                    📤 Submit Request
                  </button>
                  <button 
                    className="pvd-btn pvd-btn-back"
                    onClick={() => setShowPermissionForm(false)}
                  >
                    ← Back
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
