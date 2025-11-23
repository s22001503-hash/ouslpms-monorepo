import React, { useState, useRef } from 'react'
import ClassificationBadge from './ClassificationBadge'
import PrintConfirmationDialog from './PrintConfirmationDialog'
import PolicyViolationDialog from './PolicyViolationDialog'
import DuplicateDocumentDialog from './DuplicateDocumentDialog'
import { saveToDrive, isGoogleDriveAvailable } from '../services/googleDrive'
import './PrintWorkflow.css'

/**
 * PrintWorkflow - Enhanced print upload and approval request component
 * Handles: File upload, AI classification, policy checks, VC approval requests
 */
export default function PrintWorkflow({ userEpf, userName }) {
  const [uploadState, setUploadState] = useState('idle') // idle, uploading, classifying, results, blocked
  const [file, setFile] = useState(null)
  const [classification, setClassification] = useState(null)
  const [blockReason, setBlockReason] = useState(null)
  const [canRequestApproval, setCanRequestApproval] = useState(false)
  const [justification, setJustification] = useState('')
  const [requestSent, setRequestSent] = useState(false)
  const [showConfirmDialog, setShowConfirmDialog] = useState(false)
  const [showViolationDialog, setShowViolationDialog] = useState(false)
  const [showDuplicateDialog, setShowDuplicateDialog] = useState(false)
  const [duplicateInfo, setDuplicateInfo] = useState(null)
  const [userDailyStats, setUserDailyStats] = useState({ used: 1, limit: 10 }) // Mock data
  const fileInputRef = useRef(null)

  const handleFileSelect = async (selectedFile) => {
    if (!selectedFile) return

    setFile(selectedFile)
    setUploadState('uploading')
    setRequestSent(false)

    // Simulate file upload
    await new Promise(resolve => setTimeout(resolve, 1000))

    // Check if OCR is needed (for images/scanned PDFs)
    const needsOCR = selectedFile.type.includes('image') || selectedFile.name.toLowerCase().includes('scan')
    
    if (needsOCR) {
      setUploadState('ocr')
      await new Promise(resolve => setTimeout(resolve, 2000))
    }

    // Simulate AI classification
    setUploadState('classifying')
    await new Promise(resolve => setTimeout(2000))

    // Mock AI classification result
    const mockClassification = {
      type: 'official', // or 'personal', 'confidential'
      confidence: 0.95,
      policyCheck: {
        allowed: false,
        reason: 'daily_limit', // or 'copies_limit', 'personal_blocked'
        dailyUsed: 5,
        dailyLimit: 5,
        requestedCopies: 10,
        maxCopies: 5
      },
      duplicateCheck: {
        isDuplicate: true, // Set to true to test duplicate detection
        similarityScore: 92,
        previousDocument: {
          title: 'Lecture_Notes_Week_5.pdf',
          printedDate: '2025-11-17T10:30:00Z' // 2 days ago
        }
      }
    }

    setClassification(mockClassification)

    // Block personal documents immediately (no duplicate check)
    if (mockClassification.type === 'personal') {
      setBlockReason({
        type: 'personal',
        title: '❌ Personal Document Not Allowed',
        message: 'Personal documents cannot be printed through the EcoPrint system.',
        canRequest: false
      })
      setCanRequestApproval(false)
      setUploadState('blocked')
      return
    }

    // Check for duplicate ONLY for official documents
    if (mockClassification.type === 'official' &&
        mockClassification.duplicateCheck?.isDuplicate && 
        mockClassification.duplicateCheck?.similarityScore >= 85) {
      setDuplicateInfo(mockClassification.duplicateCheck.previousDocument)
      setShowDuplicateDialog(true)
      setUploadState('results') // Still classified as valid, but show duplicate warning
      return
    }

    // Determine policy violation scenarios (for official/confidential documents)
    // Determine policy violation scenarios (for official/confidential documents)
    if (!mockClassification.policyCheck.allowed) {
      if (mockClassification.policyCheck.reason === 'daily_limit') {
        setBlockReason({
          type: 'daily_limit',
          title: '⚠️ Daily Print Limit Reached',
          message: `You've used ${mockClassification.policyCheck.dailyUsed}/${mockClassification.policyCheck.dailyLimit} daily prints.`,
          canRequest: true
        })
        setCanRequestApproval(true)
      } else if (mockClassification.policyCheck.reason === 'copies_limit') {
        setBlockReason({
          type: 'copies_limit',
          title: '⚠️ Too Many Copies Requested',
          message: `You requested ${mockClassification.policyCheck.requestedCopies} copies. Maximum allowed: ${mockClassification.policyCheck.maxCopies}.`,
          canRequest: true
        })
        setCanRequestApproval(true)
      }
      setUploadState('blocked')
      setShowViolationDialog(true) // Show violation dialog instead of inline
    } else {
      setUploadState('results')
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const droppedFile = e.dataTransfer.files[0]
    if (droppedFile) handleFileSelect(droppedFile)
  }

  const handleDragOver = (e) => {
    e.preventDefault()
  }

  const handleSendToVC = async () => {
    if (!justification.trim()) {
      alert('Please provide a justification for your request')
      return
    }

    // TODO: Call API to send VC approval request
    console.log('Sending VC approval request:', {
      file: file.name,
      classification: classification.type,
      reason: blockReason.type,
      justification
    })

    setRequestSent(true)
  }

  const handleReset = () => {
    setUploadState('idle')
    setFile(null)
    setClassification(null)
    setBlockReason(null)
    setCanRequestApproval(false)
    setJustification('')
    setRequestSent(false)
    setShowConfirmDialog(false)
    setShowViolationDialog(false)
    setShowDuplicateDialog(false)
    setDuplicateInfo(null)
  }

  const handleDuplicatePrintAnyway = () => {
    setShowDuplicateDialog(false)
    // Proceed to normal confirmation dialog
    setShowConfirmDialog(true)
  }

  const handleDuplicateSaveToDrive = async () => {
    setShowDuplicateDialog(false)
    await handleSaveToDrive()
  }

  const handleDuplicateCancel = () => {
    setShowDuplicateDialog(false)
    handleReset()
  }

  const handleViolationPermissionRequest = async (justificationText) => {
    // TODO: Call API to send HOD approval request
    console.log('Sending HOD approval request:', {
      file: file.name,
      classification: classification.type,
      reason: blockReason.type,
      justification: justificationText
    })

    setShowViolationDialog(false)
    alert('✅ Request sent successfully! You\'ll be notified when the HOD makes a decision.')
    handleReset()
  }

  const handleViolationSaveToDrive = async () => {
    setShowViolationDialog(false)
    await handleSaveToDrive()
  }

  const handleViolationCancel = () => {
    setShowViolationDialog(false)
    handleReset()
  }

  const handleConfirmPrint = () => {
    // Show confirmation dialog instead of direct print
    setShowConfirmDialog(true)
  }

  const handleFinalPrint = async () => {
    setShowConfirmDialog(false)
    
    // TODO: Call actual print API
    console.log('Executing print job:', {
      file: file.name,
      classification: classification.type,
      userEpf,
      userName
    })

    // Show success message
    alert('✅ Print job submitted successfully!')
    
    // Update daily stats
    setUserDailyStats(prev => ({
      ...prev,
      used: prev.used + 1
    }))

    // Reset workflow
    handleReset()
  }

  const handleSaveToDrive = async () => {
    if (!file) {
      alert('❌ No file to save')
      return
    }

    // Check if Google Drive is configured
    if (!isGoogleDriveAvailable()) {
      alert('⚠️ Google Drive integration is not configured.\n\nPlease ask your administrator to set up Google Drive credentials.')
      setShowConfirmDialog(false)
      return
    }

    try {
      const result = await saveToDrive(file, {
        fileName: file.name,
        onProgress: (status) => {
          console.log('Drive upload progress:', status)
        },
        onSuccess: (data) => {
          setShowConfirmDialog(false)
          alert(`✅ ${data.message}\n\nFile: ${data.fileName}\nView in Drive: ${data.fileLink}`)
          handleReset()
        },
        onError: (error) => {
          alert(`❌ Failed to save to Google Drive:\n${error}`)
        }
      })

      if (result.success) {
        console.log('File saved to Drive:', result.fileLink)
      }
    } catch (error) {
      console.error('Error saving to Drive:', error)
      alert(`❌ Error: ${error.message || 'Failed to save to Google Drive'}`)
    }
  }

  const handleCancelPrint = () => {
    setShowConfirmDialog(false)
  }

  return (
    <div className="print-workflow">
      {/* File Upload Area */}
      {uploadState === 'idle' && (
        <div 
          className="pw-upload-zone"
          onDrop={handleDrop}
          onDragOver={handleDragOver}
        >
          <div className="pw-upload-icon">📄</div>
          <p className="pw-upload-text">
            Drag and drop your document here
          </p>
          <p className="pw-upload-subtext">or</p>
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.doc,.docx,.txt,.png,.jpg,.jpeg"
            style={{ display: 'none' }}
            onChange={(e) => handleFileSelect(e.target.files[0])}
          />
          <button 
            className="pw-upload-btn"
            onClick={() => fileInputRef.current?.click()}
          >
            Choose File
          </button>
          <p className="pw-upload-formats">
            Supported: PDF, DOCX, TXT, Images (PNG, JPG)
          </p>
        </div>
      )}

      {/* Uploading State */}
      {uploadState === 'uploading' && (
        <div className="pw-status">
          <div className="pw-spinner"></div>
          <p className="pw-status-text">Uploading {file?.name}...</p>
        </div>
      )}

      {/* OCR Processing */}
      {uploadState === 'ocr' && (
        <div className="pw-status">
          <div className="pw-spinner"></div>
          <p className="pw-status-text">📷 OCR Processing: Extracting text from scanned document...</p>
          <p className="pw-status-subtext">This may take a moment</p>
        </div>
      )}

      {/* AI Classification */}
      {uploadState === 'classifying' && (
        <div className="pw-status">
          <div className="pw-spinner"></div>
          <p className="pw-status-text">🤖 AI is analyzing your document...</p>
          <p className="pw-status-subtext">Classifying content and checking policies</p>
        </div>
      )}

      {/* Results - Allowed */}
      {uploadState === 'results' && classification && !showDuplicateDialog && (
        <div className="pw-results">
          <div className="pw-results-header">
            <h3>✅ Classification Complete</h3>
          </div>
          <div className="pw-results-body">
            <div className="pw-result-row">
              <span className="pw-label">Document:</span>
              <span className="pw-value">{file?.name}</span>
            </div>
            <div className="pw-result-row">
              <span className="pw-label">Classification:</span>
              <ClassificationBadge type={classification.type} size="large" />
            </div>
            <div className="pw-result-row">
              <span className="pw-label">Confidence:</span>
              <span className="pw-value">{(classification.confidence * 100).toFixed(0)}%</span>
            </div>
            <div className="pw-success-box">
              ✅ Document approved for printing!
            </div>
            <div className="pw-actions">
              <button className="pw-btn primary" onClick={handleConfirmPrint}>
                Confirm & Print
              </button>
              <button className="pw-btn secondary" onClick={handleReset}>Cancel</button>
            </div>
          </div>
        </div>
      )}

      {/* Blocked States */}
      {uploadState === 'blocked' && blockReason && !showViolationDialog && (
        <div className="pw-blocked">
          <div className="pw-blocked-header">
            <h3>{blockReason.title}</h3>
          </div>
          <div className="pw-blocked-body">
            <div className="pw-result-row">
              <span className="pw-label">Document:</span>
              <span className="pw-value">{file?.name}</span>
            </div>
            <div className="pw-result-row">
              <span className="pw-label">Classification:</span>
              <ClassificationBadge type={classification?.type} size="large" />
            </div>
            <div className={`pw-block-box ${blockReason.type}`}>
              <p className="pw-block-message">{blockReason.message}</p>
            </div>
            <p className="pw-processing-text">Processing your options...</p>
          </div>
        </div>
      )}

      {/* Info Box */}
      <div className="pw-info-box">
        <h4>ℹ️ How AI Classification Works:</h4>
        <ol>
          <li>Upload your document (PDF, DOCX, TXT, or images)</li>
          <li>AI analyzes content and classifies as Official/Personal/Confidential</li>
          <li>System checks print policies and daily limits</li>
          <li>If blocked due to limits, you can request VC approval</li>
          <li><strong>Note:</strong> Personal documents are always blocked (no VC override)</li>
        </ol>
      </div>

      {/* Print Confirmation Dialog */}
      <PrintConfirmationDialog
        isOpen={showConfirmDialog}
        onConfirm={handleFinalPrint}
        onCancel={handleCancelPrint}
        onSaveToDrive={handleSaveToDrive}
        fileName={file?.name}
        remainingPrints={userDailyStats.limit - userDailyStats.used}
        dailyLimit={userDailyStats.limit}
      />

      {/* Policy Violation Dialog */}
      <PolicyViolationDialog
        isOpen={showViolationDialog}
        onRequestPermission={handleViolationPermissionRequest}
        onSaveToDrive={handleViolationSaveToDrive}
        onCancel={handleViolationCancel}
        fileName={file?.name}
        violationType={blockReason?.type}
        violationMessage={blockReason?.message}
      />

      {/* Duplicate Document Dialog */}
      <DuplicateDocumentDialog
        isOpen={showDuplicateDialog}
        onPrintAnyway={handleDuplicatePrintAnyway}
        onSaveToDrive={handleDuplicateSaveToDrive}
        onCancel={handleDuplicateCancel}
        currentFileName={file?.name}
        duplicateInfo={{
          title: duplicateInfo?.title,
          printedDate: duplicateInfo?.printedDate,
          similarityScore: classification?.duplicateCheck?.similarityScore
        }}
      />
    </div>
  )
}
