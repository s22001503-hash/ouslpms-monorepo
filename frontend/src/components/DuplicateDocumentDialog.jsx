import React from 'react'
import './DuplicateDocumentDialog.css'

/**
 * DuplicateDocumentDialog - Shows when a similar document was recently printed
 * Alerts users about potential duplicates and suggests alternatives
 */
export default function DuplicateDocumentDialog({ 
  isOpen, 
  onPrintAnyway,
  onSaveToDrive,
  onCancel,
  currentFileName,
  duplicateInfo // { title, printedDate, similarityScore }
}) {
  if (!isOpen) return null

  // Calculate time difference
  const getTimeDifference = (printedDate) => {
    const now = new Date()
    const printed = new Date(printedDate)
    const diffTime = Math.abs(now - printed)
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    if (diffDays === 0) return 'today'
    if (diffDays === 1) return '1 day ago'
    if (diffDays < 7) return `${diffDays} days ago`
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
    return `${Math.floor(diffDays / 30)} months ago`
  }

  return (
    <div className="ddd-overlay">
      <div className="ddd-dialog">
        <div className="ddd-header">
          <div className="ddd-header-icon">🔄</div>
          <h2>SIMILAR DOCUMENT DETECTED</h2>
        </div>

        <div className="ddd-body">
          {/* Alert Message */}
          <p className="ddd-alert-text">
            We found a document in your print history that appears very similar to this one:
          </p>

          {/* Current Document */}
          <div className="ddd-current-doc">
            <strong>📄 Current Document:</strong>
            <span>{currentFileName}</span>
          </div>

          {/* Duplicate Info Card */}
          <div className="ddd-duplicate-card">
            <div className="ddd-duplicate-header">
              <strong>Previously Printed:</strong>
              <span className="ddd-doc-title">{duplicateInfo?.title || 'Similar Document'}</span>
            </div>
            <div className="ddd-duplicate-meta">
              <span className="ddd-meta-item">
                🕒 Printed: <strong>{getTimeDifference(duplicateInfo?.printedDate)}</strong>
              </span>
              <span className="ddd-meta-divider">|</span>
              <span className="ddd-meta-item">
                🎯 Similarity: <strong>{duplicateInfo?.similarityScore || 0}%</strong>
              </span>
            </div>
          </div>

          {/* Suggestion Section */}
          <div className="ddd-suggestion">
            <h3>💡 Suggestion:</h3>
            <p className="ddd-suggestion-text">
              You might already have a physical copy. Consider:
            </p>
            <ul className="ddd-suggestion-list">
              <li>Reviewing your existing printed version</li>
              <li>
                <strong>📧 Share a Digital Copy</strong>
                <span className="ddd-sub-text">Send via Email, WhatsApp, or Telegram</span>
              </li>
              <li>
                <strong>💾 Save for Later</strong>
                <span className="ddd-sub-text">Store it in Google Drive or OneDrive</span>
              </li>
              <li>Printing only if you need an updated copy</li>
            </ul>
          </div>

          {/* Action Buttons */}
          <div className="ddd-actions">
            <button 
              className="ddd-btn ddd-btn-print"
              onClick={onPrintAnyway}
            >
              🖨️ Print Anyway
            </button>
            <button 
              className="ddd-btn ddd-btn-drive"
              onClick={onSaveToDrive}
            >
              💾 Save to Google Drive
            </button>
            <button 
              className="ddd-btn ddd-btn-cancel"
              onClick={onCancel}
            >
              ❌ Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
