import React, { useState } from 'react'
import './PrintConfirmationDialog.css'

/**
 * PrintConfirmationDialog - Shows before executing print job for official documents
 * Displays resource usage, alternatives, and confirmation
 */
export default function PrintConfirmationDialog({ 
  isOpen, 
  onConfirm, 
  onCancel, 
  onSaveToDrive,
  fileName,
  remainingPrints = 9,
  dailyLimit = 10 
}) {
  const [isSaving, setIsSaving] = useState(false)
  const [saveStatus, setSaveStatus] = useState(null)

  if (!isOpen) return null

  const handleSaveToDrive = async () => {
    setIsSaving(true)
    setSaveStatus('Connecting to Google Drive...')
    
    try {
      await onSaveToDrive()
      setSaveStatus('Saved successfully!')
    } catch (error) {
      setSaveStatus('Failed to save')
      setIsSaving(false)
    }
  }

  const usedPrints = dailyLimit - remainingPrints
  const percentageRemaining = (remainingPrints / dailyLimit) * 100
  const percentageUsing = (1 / dailyLimit) * 100

  // Calculate progress bar blocks (10 blocks total)
  const totalBlocks = 10
  const filledBlocks = Math.floor((remainingPrints / dailyLimit) * totalBlocks)
  const emptyBlocks = totalBlocks - filledBlocks

  return (
    <div className="pcd-overlay">
      <div className="pcd-dialog">
        <div className="pcd-header">
          <h2>🖨️ PRINT CONFIRMATION</h2>
        </div>

        <div className="pcd-body">
          {/* Approval Status */}
          <div className="pcd-status">
            <div className="pcd-status-icon">✅</div>
            <div className="pcd-status-text">
              <strong>Document Approved: Official</strong>
              <div className="pcd-filename">{fileName}</div>
            </div>
          </div>

          {/* Resource Usage */}
          <div className="pcd-resources">
            <h3>📊 YOUR RESOURCES:</h3>
            <div className="pcd-progress-bar">
              <div className="pcd-progress-blocks">
                {[...Array(filledBlocks)].map((_, i) => (
                  <span key={`filled-${i}`} className="pcd-block filled">█</span>
                ))}
                {[...Array(emptyBlocks)].map((_, i) => (
                  <span key={`empty-${i}`} className="pcd-block empty">░</span>
                ))}
              </div>
              <div className="pcd-progress-label">
                {remainingPrints}/{dailyLimit} remaining ({percentageRemaining.toFixed(0)}%)
              </div>
            </div>
            <div className="pcd-usage-info">
              This print will use: <span className="pcd-block-single">█</span> 
              <span className="pcd-usage-percent">({percentageUsing.toFixed(0)}% of your allocation)</span>
            </div>
          </div>

          {/* Before You Print Tips */}
          <div className="pcd-tips">
            <h3>💡 BEFORE YOU PRINT:</h3>
            <ul>
              <li>Is this the final version of your document?</li>
              <li>Is this essential to be get printed?</li>
            </ul>
            <div className="pcd-alternatives">
              <strong>🔄 Instead of Printing, You Could Also:</strong>
              <div className="pcd-alt-options">
                <span>📱 Share via WhatsApp/Telegram/Email</span>
                <span>☁️ Save to Google Drive</span>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="pcd-actions">
            {saveStatus && (
              <div className={`pcd-status-message ${saveStatus.includes('successfully') ? 'success' : 'error'}`}>
                {saveStatus}
              </div>
            )}
            
            <button 
              className="pcd-btn pcd-btn-drive"
              onClick={handleSaveToDrive}
              disabled={isSaving}
              title="Save to Google Drive instead of printing"
            >
              {isSaving ? '⏳ Saving...' : '💾 Save to Google Drive'}
            </button>
            <button 
              className="pcd-btn pcd-btn-print"
              onClick={onConfirm}
              disabled={isSaving}
            >
              🖨️ Print Document ({remainingPrints}→{remainingPrints - 1})
            </button>
            <button 
              className="pcd-btn pcd-btn-cancel"
              onClick={onCancel}
              disabled={isSaving}
            >
              ❌ Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
