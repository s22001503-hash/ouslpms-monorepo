import React, { useState, useEffect } from 'react'
import { fetchSystemSettings, fetchSettingsRequests, proposeSettings } from '../services/api'
import './SettingsProposalTab.css'

export default function SettingsProposalTab({ adminId }) {
  const [currentSettings, setCurrentSettings] = useState({
    maxCopiesPerDocument: 0,
    maxPrintAttemptsPerDay: 0,
    maxPagesPerJob: 0,
    dailyQuota: 0,
    allowColorPrinting: false
  })

  const [proposedSettings, setProposedSettings] = useState({
    maxCopiesPerDocument: '',
    maxPrintAttemptsPerDay: '',
    maxPagesPerJob: '',
    dailyQuota: '',
    allowColorPrinting: false
  })

  const [proposals, setProposals] = useState([])
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState({ type: '', text: '' })
  const [hasPendingProposal, setHasPendingProposal] = useState(false)

  // Fetch current settings
  useEffect(() => {
    fetchCurrentSettings()
    fetchProposalHistory()
  }, [adminId])

  const fetchCurrentSettings = async () => {
    try {
      const data = await fetchSystemSettings()
      setCurrentSettings(data)
      setProposedSettings({
        maxCopiesPerDocument: data.maxCopiesPerDocument,
        maxPrintAttemptsPerDay: data.maxPrintAttemptsPerDay,
        maxPagesPerJob: data.maxPagesPerJob,
        dailyQuota: data.dailyQuota,
        allowColorPrinting: data.allowColorPrinting
      })
    } catch (error) {
      console.error('Failed to fetch settings:', error)
      // Fallback to mock data if API fails
      const mockSettings = {
        maxCopiesPerDocument: 10,
        maxPrintAttemptsPerDay: 50,
        maxPagesPerJob: 100,
        dailyQuota: 500,
        allowColorPrinting: true
      }
      setCurrentSettings(mockSettings)
      setProposedSettings(mockSettings)
    }
  }

  const fetchProposalHistory = async () => {
    try {
      const data = await fetchSettingsRequests(adminId)
      setProposals(data)
      
      // Check if there's a pending proposal
      const pending = data.some(p => p.status === 'pending')
      setHasPendingProposal(pending)
    } catch (error) {
      console.error('Failed to fetch proposals:', error)
      // Set empty array if API fails
      setProposals([])
      setHasPendingProposal(false)
    }
  }

  const handleInputChange = (field, value) => {
    setProposedSettings(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const validateProposal = () => {
    const errors = []
    
    // Validate numeric fields
    if (proposedSettings.maxCopiesPerDocument < 1 || proposedSettings.maxCopiesPerDocument > 100) {
      errors.push('Max copies per document must be between 1 and 100')
    }
    
    if (proposedSettings.maxPrintAttemptsPerDay < 1 || proposedSettings.maxPrintAttemptsPerDay > 200) {
      errors.push('Max print attempts per day must be between 1 and 200')
    }
    
    if (proposedSettings.maxPagesPerJob < 1 || proposedSettings.maxPagesPerJob > 500) {
      errors.push('Max pages per job must be between 1 and 500')
    }
    
    if (proposedSettings.dailyQuota < 1 || proposedSettings.dailyQuota > 2000) {
      errors.push('Daily quota must be between 1 and 2000')
    }
    
    // Check if anything changed
    const hasChanges = 
      proposedSettings.maxCopiesPerDocument != currentSettings.maxCopiesPerDocument ||
      proposedSettings.maxPrintAttemptsPerDay != currentSettings.maxPrintAttemptsPerDay ||
      proposedSettings.maxPagesPerJob != currentSettings.maxPagesPerJob ||
      proposedSettings.dailyQuota != currentSettings.dailyQuota ||
      proposedSettings.allowColorPrinting !== currentSettings.allowColorPrinting
    
    if (!hasChanges) {
      errors.push('No changes detected. Please modify at least one setting.')
    }
    
    return errors
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setMessage({ type: '', text: '' })
    
    // Validate
    const errors = validateProposal()
    if (errors.length > 0) {
      setMessage({ type: 'error', text: errors.join(' ') })
      return
    }
    
    setLoading(true)
    
    try {
      const result = await proposeSettings({
        adminId,
        proposedSettings: {
          maxCopiesPerDocument: parseInt(proposedSettings.maxCopiesPerDocument),
          maxPrintAttemptsPerDay: parseInt(proposedSettings.maxPrintAttemptsPerDay),
          maxPagesPerJob: parseInt(proposedSettings.maxPagesPerJob),
          dailyQuota: parseInt(proposedSettings.dailyQuota),
          allowColorPrinting: proposedSettings.allowColorPrinting
        }
      })
      
      setMessage({ 
        type: 'success', 
        text: result.message || 'Settings proposed successfully! Your proposal has been sent to the Dean for approval.' 
      })
      
      // Refresh proposal history
      await fetchProposalHistory()
      setHasPendingProposal(true)
      
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: error.message || 'Failed to submit proposal. Please try again.' 
      })
    } finally {
      setLoading(false)
    }
  }

  const getStatusBadge = (status) => {
    const badges = {
      pending: { label: 'Pending', class: 'status-pending' },
      approved: { label: 'Approved', class: 'status-approved' },
      rejected: { label: 'Rejected', class: 'status-rejected' }
    }
    return badges[status] || badges.pending
  }

  return (
    <div className="settings-proposal-tab">
      <div className="sp-header">
        <h2>Settings Proposal</h2>
        <p>Propose changes to system settings for Dean approval</p>
      </div>

      {/* Current Settings (Read-Only) */}
      <div className="sp-card">
        <div className="sp-card-header">
          <h3>Current System Settings</h3>
          <span className="sp-badge approved">Active</span>
        </div>
        <div className="sp-card-body">
          <div className="sp-settings-grid">
            <div className="sp-setting-item">
              <label>Max Copies per Document</label>
              <div className="sp-setting-value">{currentSettings.maxCopiesPerDocument}</div>
            </div>
            <div className="sp-setting-item">
              <label>Max Print Attempts per Day</label>
              <div className="sp-setting-value">{currentSettings.maxPrintAttemptsPerDay}</div>
            </div>
            <div className="sp-setting-item">
              <label>Max Pages per Job</label>
              <div className="sp-setting-value">{currentSettings.maxPagesPerJob}</div>
            </div>
            <div className="sp-setting-item">
              <label>Daily Quota (pages)</label>
              <div className="sp-setting-value">{currentSettings.dailyQuota}</div>
            </div>
            <div className="sp-setting-item">
              <label>Allow Color Printing</label>
              <div className="sp-setting-value">
                {currentSettings.allowColorPrinting ? '✅ Yes' : '❌ No'}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Proposal Form */}
      <div className="sp-card">
        <div className="sp-card-header">
          <h3>Propose New Settings</h3>
          {hasPendingProposal && (
            <span className="sp-badge pending">Pending Proposal</span>
          )}
        </div>
        <div className="sp-card-body">
          {message.text && (
            <div className={`sp-message ${message.type}`}>
              {message.text}
            </div>
          )}

          <form onSubmit={handleSubmit} className="sp-proposal-form">
            <div className="sp-form-grid">
              <div className="sp-form-group">
                <label htmlFor="maxCopies">Max Copies per Document</label>
                <input
                  id="maxCopies"
                  type="number"
                  min="1"
                  max="100"
                  value={proposedSettings.maxCopiesPerDocument}
                  onChange={(e) => handleInputChange('maxCopiesPerDocument', parseInt(e.target.value))}
                  disabled={hasPendingProposal || loading}
                  required
                />
                <span className="sp-hint">Current: {currentSettings.maxCopiesPerDocument}</span>
              </div>

              <div className="sp-form-group">
                <label htmlFor="maxAttempts">Max Print Attempts per Day</label>
                <input
                  id="maxAttempts"
                  type="number"
                  min="1"
                  max="200"
                  value={proposedSettings.maxPrintAttemptsPerDay}
                  onChange={(e) => handleInputChange('maxPrintAttemptsPerDay', parseInt(e.target.value))}
                  disabled={hasPendingProposal || loading}
                  required
                />
                <span className="sp-hint">Current: {currentSettings.maxPrintAttemptsPerDay}</span>
              </div>

              <div className="sp-form-group">
                <label htmlFor="maxPages">Max Pages per Job</label>
                <input
                  id="maxPages"
                  type="number"
                  min="1"
                  max="500"
                  value={proposedSettings.maxPagesPerJob}
                  onChange={(e) => handleInputChange('maxPagesPerJob', parseInt(e.target.value))}
                  disabled={hasPendingProposal || loading}
                  required
                />
                <span className="sp-hint">Current: {currentSettings.maxPagesPerJob}</span>
              </div>

              <div className="sp-form-group">
                <label htmlFor="dailyQuota">Daily Quota (pages)</label>
                <input
                  id="dailyQuota"
                  type="number"
                  min="1"
                  max="2000"
                  value={proposedSettings.dailyQuota}
                  onChange={(e) => handleInputChange('dailyQuota', parseInt(e.target.value))}
                  disabled={hasPendingProposal || loading}
                  required
                />
                <span className="sp-hint">Current: {currentSettings.dailyQuota}</span>
              </div>

              <div className="sp-form-group">
                <label>Allow Color Printing</label>
                <label className="sp-toggle">
                  <input
                    type="checkbox"
                    checked={proposedSettings.allowColorPrinting}
                    onChange={(e) => handleInputChange('allowColorPrinting', e.target.checked)}
                    disabled={hasPendingProposal || loading}
                  />
                  <span className="sp-toggle-slider"></span>
                </label>
                <span className="sp-hint">
                  Current: {currentSettings.allowColorPrinting ? 'Enabled' : 'Disabled'}
                </span>
              </div>
            </div>

            <div className="sp-form-actions">
              <button
                type="submit"
                className="sp-btn primary"
                disabled={hasPendingProposal || loading}
              >
                {loading ? 'Submitting...' : 'Submit Proposal'}
              </button>
              {hasPendingProposal && (
                <p className="sp-pending-note">
                  You have a pending proposal. Please wait for Dean approval before submitting a new one.
                </p>
              )}
            </div>
          </form>
        </div>
      </div>

      {/* Proposal History */}
      <div className="sp-card">
        <div className="sp-card-header">
          <h3>Proposal History</h3>
        </div>
        <div className="sp-card-body">
          {proposals.length === 0 ? (
            <div className="sp-empty-state">
              <span className="sp-empty-icon">📋</span>
              <p>No proposals yet</p>
            </div>
          ) : (
            <div className="sp-history-table">
              <table>
                <thead>
                  <tr>
                    <th>Submitted</th>
                    <th>Proposed Changes</th>
                    <th>Status</th>
                    <th>Reviewed</th>
                    <th>Reviewer</th>
                  </tr>
                </thead>
                <tbody>
                  {proposals.map(proposal => {
                    const badge = getStatusBadge(proposal.status)
                    return (
                      <tr key={proposal.id}>
                        <td>{proposal.submittedAt}</td>
                        <td>
                          <div className="sp-changes">
                            {Object.entries(proposal.proposedSettings).map(([key, value]) => (
                              <div key={key} className="sp-change-item">
                                <strong>{key}:</strong> {value.toString()}
                              </div>
                            ))}
                          </div>
                        </td>
                        <td>
                          <span className={`sp-status-badge ${badge.class}`}>
                            {badge.label}
                          </span>
                        </td>
                        <td>{proposal.reviewedAt || '—'}</td>
                        <td>{proposal.reviewedBy || '—'}</td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
