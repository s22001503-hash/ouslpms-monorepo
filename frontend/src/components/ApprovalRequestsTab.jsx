import React, { useState, useEffect } from 'react'
import ClassificationBadge from './ClassificationBadge'
import './ApprovalRequestsTab.css'

/**
 * ApprovalRequestsTab - VC Dashboard tab for reviewing user print approval requests
 */
export default function ApprovalRequestsTab({ vcId, vcName }) {
  const [requests, setRequests] = useState([])
  const [filter, setFilter] = useState('pending') // pending, approved, rejected, all
  const [selectedRequest, setSelectedRequest] = useState(null)
  const [vcNotes, setVcNotes] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadRequests()
  }, [filter])

  const loadRequests = async () => {
    // TODO: Replace with actual API call
    const mockRequests = [
      {
        id: 'REQ001',
        userId: '12345',
        userName: 'John Smith',
        userEpf: '50123',
        documentName: 'Research_Paper_Final.pdf',
        classification: 'official',
        blockReason: 'daily_limit',
        blockDetails: 'User has used 5/5 daily prints',
        userJustification: 'Urgent research materials needed for tomorrow\'s conference presentation. This is critical for my academic work.',
        requestedAt: '2024-11-12 09:30 AM',
        status: 'pending',
        copies: 10,
        pages: 45
      },
      {
        id: 'REQ002',
        userId: '12346',
        userName: 'Sarah Johnson',
        userEpf: '50124',
        documentName: 'Lecture_Notes_Week5.pdf',
        classification: 'official',
        blockReason: 'copies_limit',
        blockDetails: 'Requested 15 copies, maximum allowed is 5',
        userJustification: 'Need copies for all students in my tutorial group (12 students). Class materials for next session.',
        requestedAt: '2024-11-12 08:15 AM',
        status: 'pending',
        copies: 15,
        pages: 8
      },
      {
        id: 'REQ003',
        userId: '12347',
        userName: 'Michael Brown',
        userEpf: '50125',
        documentName: 'Assignment_Guidelines.pdf',
        classification: 'official',
        blockReason: 'daily_limit',
        blockDetails: 'User has used 5/5 daily prints',
        userJustification: 'Updated assignment guidelines that need to be distributed urgently.',
        requestedAt: '2024-11-11 04:20 PM',
        status: 'approved',
        vcNotes: 'Approved for educational purposes.',
        vcName: 'Dr. Vice Chancellor',
        decidedAt: '2024-11-11 04:45 PM',
        copies: 5,
        pages: 3
      }
    ]

    // Filter requests
    const filtered = filter === 'all' 
      ? mockRequests 
      : mockRequests.filter(r => r.status === filter)
    
    setRequests(filtered)
  }

  const handleApprove = async (requestId) => {
    setLoading(true)
    // TODO: Call API to approve request
    console.log('Approving request:', requestId, 'with notes:', vcNotes)
    
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    setLoading(false)
    setSelectedRequest(null)
    setVcNotes('')
    loadRequests()
  }

  const handleReject = async (requestId) => {
    if (!vcNotes.trim()) {
      alert('Please provide a reason for rejection')
      return
    }

    setLoading(true)
    // TODO: Call API to reject request
    console.log('Rejecting request:', requestId, 'with reason:', vcNotes)
    
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    setLoading(false)
    setSelectedRequest(null)
    setVcNotes('')
    loadRequests()
  }

  const getBlockReasonLabel = (reason) => {
    const labels = {
      daily_limit: '📅 Daily Limit Exceeded',
      copies_limit: '📄 Copy Limit Exceeded',
      personal: '🚫 Personal Document'
    }
    return labels[reason] || reason
  }

  return (
    <div className="approval-requests-tab">
      <div className="art-header">
        <h2>📋 Approval Requests</h2>
        <p>Review and approve/reject user print requests</p>
      </div>

      {/* Filter Tabs */}
      <div className="art-filters">
        <button 
          className={`art-filter-btn ${filter === 'pending' ? 'active' : ''}`}
          onClick={() => setFilter('pending')}
        >
          ⏳ Pending
        </button>
        <button 
          className={`art-filter-btn ${filter === 'approved' ? 'active' : ''}`}
          onClick={() => setFilter('approved')}
        >
          ✅ Approved
        </button>
        <button 
          className={`art-filter-btn ${filter === 'rejected' ? 'active' : ''}`}
          onClick={() => setFilter('rejected')}
        >
          ❌ Rejected
        </button>
        <button 
          className={`art-filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          📋 All
        </button>
      </div>

      {/* Requests List */}
      <div className="art-requests-list">
        {requests.length === 0 ? (
          <div className="art-empty">
            <div className="art-empty-icon">📭</div>
            <p>No {filter !== 'all' ? filter : ''} requests found</p>
          </div>
        ) : (
          requests.map(request => (
            <div key={request.id} className={`art-request-card art-${request.status}`}>
              <div className="art-card-header">
                <div className="art-card-title">
                  <span className="art-request-id">#{request.id}</span>
                  <span className={`art-status-badge art-status-${request.status}`}>
                    {request.status.toUpperCase()}
                  </span>
                </div>
                <span className="art-timestamp">{request.requestedAt}</span>
              </div>

              <div className="art-card-body">
                {/* User Info */}
                <div className="art-section">
                  <div className="art-row">
                    <span className="art-label">User:</span>
                    <span className="art-value">{request.userName} (EPF: {request.userEpf})</span>
                  </div>
                  <div className="art-row">
                    <span className="art-label">Document:</span>
                    <span className="art-value">{request.documentName}</span>
                  </div>
                  <div className="art-row">
                    <span className="art-label">Classification:</span>
                    <ClassificationBadge type={request.classification} />
                  </div>
                  <div className="art-row">
                    <span className="art-label">Details:</span>
                    <span className="art-value">{request.pages} pages × {request.copies} copies</span>
                  </div>
                </div>

                {/* Block Reason */}
                <div className="art-section">
                  <div className="art-block-reason">
                    <div className="art-block-title">
                      {getBlockReasonLabel(request.blockReason)}
                    </div>
                    <div className="art-block-details">
                      {request.blockDetails}
                    </div>
                  </div>
                </div>

                {/* User Justification */}
                <div className="art-section">
                  <div className="art-justification">
                    <div className="art-justification-header">💬 User Justification:</div>
                    <div className="art-justification-text">
                      "{request.userJustification}"
                    </div>
                  </div>
                </div>

                {/* Decision Section (for approved/rejected) */}
                {request.status !== 'pending' && (
                  <div className="art-section">
                    <div className={`art-decision art-decision-${request.status}`}>
                      <div className="art-decision-header">
                        {request.status === 'approved' ? '✅ Approved by' : '❌ Rejected by'} {request.vcName}
                      </div>
                      {request.vcNotes && (
                        <div className="art-decision-notes">
                          <strong>Notes:</strong> {request.vcNotes}
                        </div>
                      )}
                      <div className="art-decision-time">
                        {request.decidedAt}
                      </div>
                    </div>
                  </div>
                )}

                {/* Actions (for pending) */}
                {request.status === 'pending' && (
                  <div className="art-actions">
                    {selectedRequest === request.id ? (
                      <div className="art-action-form">
                        <textarea
                          className="art-notes-input"
                          placeholder="Add notes (optional for approval, required for rejection)..."
                          value={vcNotes}
                          onChange={(e) => setVcNotes(e.target.value)}
                          rows={3}
                        />
                        <div className="art-action-buttons">
                          <button 
                            className="art-btn approve"
                            onClick={() => handleApprove(request.id)}
                            disabled={loading}
                          >
                            {loading ? 'Processing...' : '✅ Approve'}
                          </button>
                          <button 
                            className="art-btn reject"
                            onClick={() => handleReject(request.id)}
                            disabled={loading}
                          >
                            {loading ? 'Processing...' : '❌ Reject'}
                          </button>
                          <button 
                            className="art-btn cancel"
                            onClick={() => {
                              setSelectedRequest(null)
                              setVcNotes('')
                            }}
                            disabled={loading}
                          >
                            Cancel
                          </button>
                        </div>
                      </div>
                    ) : (
                      <button 
                        className="art-btn review"
                        onClick={() => setSelectedRequest(request.id)}
                      >
                        Review Request
                      </button>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
