import React, { useState, useEffect } from 'react'
import './PolicyManagementTab.css'

export default function PolicyManagementTab({ vcId }) {
  const [proposals, setProposals] = useState([])
  const [filter, setFilter] = useState('pending') // 'pending', 'approved', 'rejected', 'all'
  const [loading, setLoading] = useState(false)
  const [reviewNotes, setReviewNotes] = useState({})

  useEffect(() => {
    loadProposals()
  }, [])

  const loadProposals = async () => {
    setLoading(true)
    try {
      // TODO: Replace with actual API call
      // const data = await getPolicyProposals()
      const mockData = [
        // Global policy proposals
        {
          id: 'GP001',
          type: 'global',
          adminName: 'Admin User',
          adminEpf: '50001',
          department: 'IT Department',
          submittedAt: '2025-11-10T14:30:00Z',
          status: 'pending',
          justification: 'High demand during exam season. Students need more prints for study materials.',
          changes: {
            maxAttemptsPerDay: { current: 5, proposed: 7 },
            maxCopiesPerDoc: { current: 5, proposed: 8 }
          },
          vcDecision: null
        },
        // Special user policy proposals
        {
          id: 'SP001',
          type: 'special_user',
          adminName: 'Admin User',
          adminEpf: '50001',
          department: 'IT Department',
          submittedAt: '2025-11-11T09:00:00Z',
          status: 'pending',
          targetEPF: '60025',
          targetName: 'Maria Research',
          targetDept: 'Computer Science',
          justification: 'Research assistant needs higher limits for daily research paper printing.',
          proposedPolicy: {
            maxAttemptsPerDay: 15,
            maxCopiesPerDoc: 20
          },
          vcDecision: null
        },
        {
          id: 'SP002',
          type: 'special_user',
          adminName: 'System Admin',
          adminEpf: '50002',
          department: 'Administration',
          submittedAt: '2025-11-09T10:15:00Z',
          status: 'approved',
          targetEPF: '60089',
          targetName: 'John Professor',
          targetDept: 'Engineering',
          justification: 'Professor needs higher limits for course material distribution.',
          proposedPolicy: {
            maxAttemptsPerDay: 20,
            maxCopiesPerDoc: 25
          },
          vcDecision: {
            decision: 'approved',
            notes: 'Approved for academic purposes. Valid for one semester.',
            decidedBy: 'HOD Office',
            decidedAt: '2025-11-09T14:00:00Z'
          }
        },
        {
          id: 'GP002',
          type: 'global',
          adminName: 'Senior Admin',
          adminEpf: '50003',
          department: 'Academic Affairs',
          submittedAt: '2025-11-08T16:45:00Z',
          status: 'approved',
          justification: 'General increase needed based on usage analysis.',
          changes: {
            maxAttemptsPerDay: { current: 5, proposed: 6 }
          },
          vcDecision: {
            decision: 'approved',
            notes: 'Approved. Will monitor usage patterns.',
            decidedBy: 'HOD Office',
            decidedAt: '2025-11-09T09:00:00Z'
          }
        },
        {
          id: 'SP003',
          type: 'special_user',
          adminName: 'Network Admin',
          adminEpf: '50004',
          department: 'IT Department',
          submittedAt: '2025-11-07T11:20:00Z',
          status: 'rejected',
          targetEPF: '60150',
          targetName: 'Test User',
          targetDept: 'Administration',
          justification: 'User requested unlimited prints.',
          proposedPolicy: {
            maxAttemptsPerDay: 100,
            maxCopiesPerDoc: 100
          },
          vcDecision: {
            decision: 'rejected',
            notes: 'Limits too high without sufficient justification. Please resubmit with reasonable values.',
            decidedBy: 'HOD Office',
            decidedAt: '2025-11-07T15:30:00Z'
          }
        }
      ]
      setProposals(mockData)
    } catch (error) {
      console.error('Failed to load policy proposals:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleApprove = async (proposalId) => {
    const notes = reviewNotes[proposalId] || ''
    try {
      // TODO: Replace with actual API call
      // await approvePolicyProposal(proposalId, vcId, notes)
      console.log('Approving proposal:', proposalId, 'with notes:', notes)
      
      // Update local state
      setProposals(prevProposals =>
        prevProposals.map(p =>
          p.id === proposalId
            ? {
                ...p,
                status: 'approved',
                vcDecision: {
                  decision: 'approved',
                  notes: notes || 'Approved',
                  decidedBy: 'HOD Office',
                  decidedAt: new Date().toISOString()
                }
              }
            : p
        )
      )
      setReviewNotes(prev => ({ ...prev, [proposalId]: '' }))
    } catch (error) {
      console.error('Failed to approve proposal:', error)
      alert('Failed to approve proposal. Please try again.')
    }
  }

  const handleReject = async (proposalId) => {
    const notes = reviewNotes[proposalId] || ''
    if (!notes.trim()) {
      alert('Please provide a reason for rejection')
      return
    }
    
    try {
      // TODO: Replace with actual API call
      // await rejectPolicyProposal(proposalId, vcId, notes)
      console.log('Rejecting proposal:', proposalId, 'with notes:', notes)
      
      // Update local state
      setProposals(prevProposals =>
        prevProposals.map(p =>
          p.id === proposalId
            ? {
                ...p,
                status: 'rejected',
                vcDecision: {
                  decision: 'rejected',
                  notes: notes,
                  decidedBy: 'HOD Office',
                  decidedAt: new Date().toISOString()
                }
              }
            : p
        )
      )
      setReviewNotes(prev => ({ ...prev, [proposalId]: '' }))
    } catch (error) {
      console.error('Failed to reject proposal:', error)
      alert('Failed to reject proposal. Please try again.')
    }
  }

  const getFieldLabel = (field) => {
    const labels = {
      maxAttemptsPerDay: 'Max Print Attempts per Day',
      maxCopiesPerDoc: 'Max Copies per Document',
      userDailyLimit: 'User Daily Page Limit',
      userMaxCopies: 'User Max Copies',
      staffLimits: 'Staff Daily Limit',
      vcLimits: 'HOD Daily Limit',
      allowPersonalDocs: 'Allow Personal Documents',
      maxFileSize: 'Max File Size (MB)',
      autoBlockThreshold: 'Auto-block Threshold'
    }
    return labels[field] || field
  }

  const formatValue = (value) => {
    if (typeof value === 'boolean') return value ? 'Yes' : 'No'
    return value
  }

  const renderProposalChanges = (proposal) => {
    if (proposal.type === 'global') {
      // Global policy changes
      return (
        <div className="pmt-changes-list">
          {Object.entries(proposal.changes).map(([field, change]) => (
            <div key={field} className="pmt-change-item">
              <div className="pmt-field-label">{getFieldLabel(field)}</div>
              <div className="pmt-change-values">
                <span className="pmt-current-value">{formatValue(change.current)}</span>
                <span className="pmt-arrow">→</span>
                <span className="pmt-proposed-value">{formatValue(change.proposed)}</span>
              </div>
            </div>
          ))}
        </div>
      )
    } else {
      // Special user policy
      return (
        <div className="pmt-special-user-policy">
          <div className="pmt-user-details">
            <h5>👤 Target User</h5>
            <div className="pmt-user-info-card">
              <div><strong>Name:</strong> {proposal.targetName}</div>
              <div><strong>EPF:</strong> {proposal.targetEPF}</div>
              <div><strong>Department:</strong> {proposal.targetDept}</div>
            </div>
          </div>
          <div className="pmt-policy-limits">
            <h5>📋 Proposed Special Limits</h5>
            <div className="pmt-changes-list">
              <div className="pmt-change-item">
                <div className="pmt-field-label">Max Print Attempts per Day</div>
                <div className="pmt-proposed-value">{proposal.proposedPolicy.maxAttemptsPerDay}</div>
              </div>
              <div className="pmt-change-item">
                <div className="pmt-field-label">Max Copies per Document</div>
                <div className="pmt-proposed-value">{proposal.proposedPolicy.maxCopiesPerDoc}</div>
              </div>
            </div>
          </div>
        </div>
      )
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffMs = now - date
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMs / 3600000)
    const diffDays = Math.floor(diffMs / 86400000)

    if (diffMins < 60) return `${diffMins} minutes ago`
    if (diffHours < 24) return `${diffHours} hours ago`
    if (diffDays < 7) return `${diffDays} days ago`
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
  }

  const filteredProposals = proposals.filter(p => {
    if (filter === 'all') return true
    return p.status === filter
  })

  const pendingCount = proposals.filter(p => p.status === 'pending').length
  const approvedCount = proposals.filter(p => p.status === 'approved').length
  const rejectedCount = proposals.filter(p => p.status === 'rejected').length

  return (
    <div className="policy-management-tab">
      <div className="pmt-header">
        <div>
          <h2>Policy Change Requests</h2>
          <p>Review and approve policy changes proposed by administrators</p>
        </div>
        <button className="pmt-refresh-btn" onClick={loadProposals} disabled={loading}>
          🔄 {loading ? 'Loading...' : 'Refresh'}
        </button>
      </div>

      {/* Filter Tabs */}
      <div className="pmt-filters">
        <button
          className={`pmt-filter-tab ${filter === 'pending' ? 'active' : ''}`}
          onClick={() => setFilter('pending')}
        >
          ⏳ Pending ({pendingCount})
        </button>
        <button
          className={`pmt-filter-tab ${filter === 'approved' ? 'active' : ''}`}
          onClick={() => setFilter('approved')}
        >
          ✅ Approved ({approvedCount})
        </button>
        <button
          className={`pmt-filter-tab ${filter === 'rejected' ? 'active' : ''}`}
          onClick={() => setFilter('rejected')}
        >
          ❌ Rejected ({rejectedCount})
        </button>
        <button
          className={`pmt-filter-tab ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          📋 All ({proposals.length})
        </button>
      </div>

      {/* Proposals List */}
      <div className="pmt-proposals-list">
        {filteredProposals.length === 0 ? (
          <div className="pmt-empty-state">
            <div className="pmt-empty-icon">📭</div>
            <p>No {filter !== 'all' ? filter : ''} policy proposals found</p>
          </div>
        ) : (
          filteredProposals.map(proposal => (
            <div key={proposal.id} className={`pmt-proposal-card ${proposal.status}`}>
              <div className="pmt-proposal-header">
                <div className="pmt-proposal-admin">
                  <div className="pmt-admin-icon">👤</div>
                  <div>
                    <div className="pmt-admin-name">{proposal.adminName}</div>
                    <div className="pmt-admin-details">
                      EPF: {proposal.adminEpf} • {proposal.department}
                    </div>
                  </div>
                </div>
                <div className="pmt-proposal-meta">
                  <span className={`pmt-type-badge ${proposal.type}`}>
                    {proposal.type === 'global' ? '🌐 Global Policy' : '👤 Special User'}
                  </span>
                  <span className={`pmt-status-badge ${proposal.status}`}>
                    {proposal.status === 'pending' && '⏳ Pending'}
                    {proposal.status === 'approved' && '✅ Approved'}
                    {proposal.status === 'rejected' && '❌ Rejected'}
                  </span>
                  <div className="pmt-timestamp">{formatDate(proposal.submittedAt)}</div>
                </div>
              </div>

              <div className="pmt-proposal-body">
                <div className="pmt-section">
                  <h4>📝 {proposal.type === 'global' ? 'Proposed Changes' : 'Special Policy Request'}</h4>
                  {renderProposalChanges(proposal)}
                </div>

                <div className="pmt-section">
                  <h4>💡 Justification</h4>
                  <p className="pmt-justification">{proposal.justification}</p>
                </div>

                {proposal.status === 'pending' ? (
                  <div className="pmt-review-section">
                    <h4>✍️ Your Review</h4>
                    <textarea
                      className="pmt-review-notes"
                      placeholder="Add notes for your decision (optional for approval, required for rejection)..."
                      value={reviewNotes[proposal.id] || ''}
                      onChange={(e) =>
                        setReviewNotes(prev => ({ ...prev, [proposal.id]: e.target.value }))
                      }
                      rows={3}
                    />
                    <div className="pmt-review-actions">
                      <button
                        className="pmt-btn approve"
                        onClick={() => handleApprove(proposal.id)}
                      >
                        ✅ Approve Changes
                      </button>
                      <button
                        className="pmt-btn reject"
                        onClick={() => handleReject(proposal.id)}
                      >
                        ❌ Reject Changes
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="pmt-decision-section">
                    <h4>🎯 HOD Decision</h4>
                    <div className={`pmt-decision-card ${proposal.vcDecision.decision}`}>
                      <div className="pmt-decision-header">
                        <span className={`pmt-decision-badge ${proposal.vcDecision.decision}`}>
                          {proposal.vcDecision.decision === 'approved' ? '✅ Approved' : '❌ Rejected'}
                        </span>
                        <span className="pmt-decision-date">
                          {formatDate(proposal.vcDecision.decidedAt)}
                        </span>
                      </div>
                      <p className="pmt-decision-notes">{proposal.vcDecision.notes}</p>
                      <div className="pmt-decision-by">— {proposal.vcDecision.decidedBy}</div>
                    </div>
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
