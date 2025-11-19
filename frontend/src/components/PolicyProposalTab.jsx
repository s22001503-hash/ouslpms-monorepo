import React, { useState, useEffect } from 'react'
import { getUserByEPF, proposePolicyChange } from '../services/api'
import './PolicyProposalTab.css'

/**
 * PolicyProposalTab - Simplified admin interface for proposing policy changes
 * Features:
 * 1. Global Policy Changes (Max Attempts/Day, Max Copies/Doc)
 * 2. Special User Policies (individual user overrides)
 * 3. View all proposals (combined)
 */
export default function PolicyProposalTab({ adminId }) {
  const [activeSection, setActiveSection] = useState('global') // 'global', 'special', 'all'
  
  // Global Policy State
  const [currentPolicies, setCurrentPolicies] = useState({
    maxAttemptsPerDay: 5,
    maxCopiesPerDoc: 5
  })
  const [proposedPolicies, setProposedPolicies] = useState({
    maxAttemptsPerDay: 5,
    maxCopiesPerDoc: 5
  })
  const [globalJustification, setGlobalJustification] = useState('')
  const [globalLoading, setGlobalLoading] = useState(false)
  const [globalMessage, setGlobalMessage] = useState(null)
  
  // Special User Policy State
  const [searchEpf, setSearchEpf] = useState('')
  const [selectedUser, setSelectedUser] = useState(null)
  const [searchLoading, setSearchLoading] = useState(false)
  const [specialPolicies, setSpecialPolicies] = useState({
    maxAttemptsPerDay: 5,
    maxCopiesPerDoc: 5
  })
  const [specialJustification, setSpecialJustification] = useState('')
  const [specialLoading, setSpecialLoading] = useState(false)
  const [specialMessage, setSpecialMessage] = useState(null)
  
  // Proposals Lists
  const [globalProposals, setGlobalProposals] = useState([])
  const [specialProposals, setSpecialProposals] = useState([])
  const [filterStatus, setFilterStatus] = useState('all') // 'pending', 'approved', 'rejected', 'all'

  useEffect(() => {
    loadCurrentPolicies()
    loadProposals()
  }, [])

  const loadCurrentPolicies = async () => {
    // TODO: Replace with actual API call
    // const data = await getCurrentPolicies()
    const mockPolicies = {
      maxAttemptsPerDay: 5,
      maxCopiesPerDoc: 5
    }
    setCurrentPolicies(mockPolicies)
    setProposedPolicies(mockPolicies)
  }

  const loadProposals = async () => {
    // TODO: Replace with actual API call
    // const data = await getPolicyProposals()
    const mockGlobalProposals = [
      {
        id: 'GP001',
        type: 'global',
        adminEPF: '50001',
        adminName: 'Admin User',
        submittedAt: '2025-11-10T14:30:00Z',
        status: 'pending',
        changes: {
          maxAttemptsPerDay: { current: 5, proposed: 7 },
          maxCopiesPerDoc: { current: 5, proposed: 8 }
        },
        justification: 'High demand during exam season. Students need more prints.',
        vcDecision: null
      }
    ]

    const mockSpecialProposals = [
      {
        id: 'SP001',
        type: 'special_user',
        adminEPF: '50001',
        adminName: 'Admin User',
        targetEPF: '60025',
        targetName: 'Maria Research',
        targetDept: 'Computer Science',
        submittedAt: '2025-11-11T09:00:00Z',
        status: 'pending',
        proposedPolicy: {
          maxAttemptsPerDay: 15,
          maxCopiesPerDoc: 20
        },
        justification: 'Research assistant needs higher limits for daily research paper printing.',
        vcDecision: null
      }
    ]

    setGlobalProposals(mockGlobalProposals)
    setSpecialProposals(mockSpecialProposals)
  }

  const handleSearchUser = async () => {
    if (!searchEpf.trim()) {
      setSpecialMessage({ type: 'error', text: 'Please enter an EPF number' })
      return
    }

    setSearchLoading(true)
    setSpecialMessage(null)
    
    try {
      // TODO: Replace with actual API call
      // const user = await getUserByEPF(searchEpf)
      
      // Mock data
      const mockUser = {
        epf: searchEpf,
        name: 'John Doe',
        email: 'john.doe@ousl.lk',
        department: 'Computer Science',
        role: 'user'
      }
      
      setSelectedUser(mockUser)
      setSpecialPolicies({
        maxAttemptsPerDay: currentPolicies.maxAttemptsPerDay,
        maxCopiesPerDoc: currentPolicies.maxCopiesPerDoc
      })
    } catch (error) {
      setSpecialMessage({ type: 'error', text: 'User not found' })
      setSelectedUser(null)
    } finally {
      setSearchLoading(false)
    }
  }

  const handleSubmitGlobalProposal = async (e) => {
    e.preventDefault()
    
    if (!globalJustification.trim()) {
      setGlobalMessage({ type: 'error', text: 'Please provide justification' })
      return
    }

    const changes = {}
    if (proposedPolicies.maxAttemptsPerDay !== currentPolicies.maxAttemptsPerDay) {
      changes.maxAttemptsPerDay = {
        current: currentPolicies.maxAttemptsPerDay,
        proposed: proposedPolicies.maxAttemptsPerDay
      }
    }
    if (proposedPolicies.maxCopiesPerDoc !== currentPolicies.maxCopiesPerDoc) {
      changes.maxCopiesPerDoc = {
        current: currentPolicies.maxCopiesPerDoc,
        proposed: proposedPolicies.maxCopiesPerDoc
      }
    }

    if (Object.keys(changes).length === 0) {
      setGlobalMessage({ type: 'error', text: 'No changes detected' })
      return
    }

    setGlobalLoading(true)
    setGlobalMessage(null)

    try {
      // TODO: Replace with actual API call
      // await proposePolicyChange({ type: 'global', changes, justification: globalJustification, adminId })
      
      setGlobalMessage({ type: 'success', text: 'Global policy proposal submitted for VC approval!' })
      setGlobalJustification('')
      setProposedPolicies(currentPolicies)
      
      // Reload proposals
      setTimeout(() => loadProposals(), 1000)
    } catch (error) {
      setGlobalMessage({ type: 'error', text: error.message || 'Failed to submit proposal' })
    } finally {
      setGlobalLoading(false)
    }
  }

  const handleSubmitSpecialProposal = async (e) => {
    e.preventDefault()
    
    if (!selectedUser) {
      setSpecialMessage({ type: 'error', text: 'Please search and select a user first' })
      return
    }

    if (!specialJustification.trim()) {
      setSpecialMessage({ type: 'error', text: 'Please provide justification' })
      return
    }

    setSpecialLoading(true)
    setSpecialMessage(null)

    try {
      // TODO: Replace with actual API call
      // await proposePolicyChange({ 
      //   type: 'special_user', 
      //   targetEPF: selectedUser.epf,
      //   proposedPolicy: specialPolicies, 
      //   justification: specialJustification, 
      //   adminId 
      // })
      
      setSpecialMessage({ type: 'success', text: `Special policy proposal for ${selectedUser.name} submitted for VC approval!` })
      setSpecialJustification('')
      setSearchEpf('')
      setSelectedUser(null)
      
      // Reload proposals
      setTimeout(() => loadProposals(), 1000)
    } catch (error) {
      setSpecialMessage({ type: 'error', text: error.message || 'Failed to submit proposal' })
    } finally {
      setSpecialLoading(false)
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const allProposals = [...globalProposals, ...specialProposals]
    .filter(p => filterStatus === 'all' || p.status === filterStatus)
    .sort((a, b) => new Date(b.submittedAt) - new Date(a.submittedAt))

  return (
    <div className="policy-proposal-tab">
      <div className="ppt-header">
        <h2>Policy Proposals</h2>
        <p>Propose changes to global policies or request special user policies</p>
      </div>

      {/* Section Tabs */}
      <div className="ppt-section-tabs">
        <button
          className={`ppt-tab ${activeSection === 'global' ? 'active' : ''}`}
          onClick={() => setActiveSection('global')}
        >
          🌐 Global Policy Changes
        </button>
        <button
          className={`ppt-tab ${activeSection === 'special' ? 'active' : ''}`}
          onClick={() => setActiveSection('special')}
        >
          👤 Special User Policies
        </button>
        <button
          className={`ppt-tab ${activeSection === 'all' ? 'active' : ''}`}
          onClick={() => setActiveSection('all')}
        >
          📋 All Proposals ({allProposals.length})
        </button>
      </div>

      {/* Global Policy Changes Section */}
      {activeSection === 'global' && (
        <div className="ppt-section">
          <div className="ppt-current-policies">
            <h3>📊 Current Global Policies</h3>
            <div className="ppt-policy-cards">
              <div className="ppt-policy-card">
                <div className="ppt-policy-label">Max Print Attempts per Day</div>
                <div className="ppt-policy-value">{currentPolicies.maxAttemptsPerDay}</div>
              </div>
              <div className="ppt-policy-card">
                <div className="ppt-policy-label">Max Copies per Document</div>
                <div className="ppt-policy-value">{currentPolicies.maxCopiesPerDoc}</div>
              </div>
            </div>
          </div>

          <div className="ppt-proposal-form">
            <h3>✏️ Propose Global Policy Changes</h3>
            
            {globalMessage && (
              <div className={`ppt-message ${globalMessage.type}`}>
                {globalMessage.text}
              </div>
            )}

            <form onSubmit={handleSubmitGlobalProposal}>
              <div className="ppt-form-grid">
                <div className="ppt-form-row">
                  <label>Max Print Attempts per Day</label>
                  <div className="ppt-comparison">
                    <input 
                      type="number"
                      min="1"
                      max="100"
                      value={proposedPolicies.maxAttemptsPerDay}
                      onChange={(e) => setProposedPolicies(prev => ({
                        ...prev,
                        maxAttemptsPerDay: parseInt(e.target.value)
                      }))}
                      className={proposedPolicies.maxAttemptsPerDay !== currentPolicies.maxAttemptsPerDay ? 'changed' : ''}
                    />
                    {proposedPolicies.maxAttemptsPerDay !== currentPolicies.maxAttemptsPerDay && (
                      <span className="ppt-change-indicator">
                        {currentPolicies.maxAttemptsPerDay} → {proposedPolicies.maxAttemptsPerDay}
                      </span>
                    )}
                  </div>
                </div>

                <div className="ppt-form-row">
                  <label>Max Copies per Document</label>
                  <div className="ppt-comparison">
                    <input 
                      type="number"
                      min="1"
                      max="100"
                      value={proposedPolicies.maxCopiesPerDoc}
                      onChange={(e) => setProposedPolicies(prev => ({
                        ...prev,
                        maxCopiesPerDoc: parseInt(e.target.value)
                      }))}
                      className={proposedPolicies.maxCopiesPerDoc !== currentPolicies.maxCopiesPerDoc ? 'changed' : ''}
                    />
                    {proposedPolicies.maxCopiesPerDoc !== currentPolicies.maxCopiesPerDoc && (
                      <span className="ppt-change-indicator">
                        {currentPolicies.maxCopiesPerDoc} → {proposedPolicies.maxCopiesPerDoc}
                      </span>
                    )}
                  </div>
                </div>
              </div>

              <div className="ppt-form-row full-width">
                <label>Justification *</label>
                <textarea
                  value={globalJustification}
                  onChange={(e) => setGlobalJustification(e.target.value)}
                  placeholder="Explain why these changes are needed..."
                  rows={4}
                  required
                />
              </div>

              <div className="ppt-form-actions">
                <button type="submit" className="ppt-btn primary" disabled={globalLoading}>
                  {globalLoading ? '⏳ Submitting...' : '📤 Submit for VC Approval'}
                </button>
                <button 
                  type="button" 
                  className="ppt-btn secondary"
                  onClick={() => {
                    setProposedPolicies(currentPolicies)
                    setGlobalJustification('')
                    setGlobalMessage(null)
                  }}
                  disabled={globalLoading}
                >
                  🔄 Reset
                </button>
              </div>
            </form>
          </div>

          {/* Global Proposals List */}
          <div className="ppt-proposals-list">
            <h3>📋 Global Policy Proposals</h3>
            {globalProposals.length === 0 ? (
              <div className="ppt-empty-state">No global proposals yet</div>
            ) : (
              globalProposals.map(proposal => (
                <div key={proposal.id} className={`ppt-proposal-card ${proposal.status}`}>
                  <div className="ppt-proposal-header">
                    <span className={`ppt-status-badge ${proposal.status}`}>
                      {proposal.status === 'pending' && '⏳ Pending'}
                      {proposal.status === 'approved' && '✅ Approved'}
                      {proposal.status === 'rejected' && '❌ Rejected'}
                    </span>
                    <span className="ppt-proposal-date">{formatDate(proposal.submittedAt)}</span>
                  </div>
                  <div className="ppt-proposal-changes">
                    {Object.entries(proposal.changes).map(([key, change]) => (
                      <div key={key} className="ppt-change-item">
                        <span className="ppt-change-label">
                          {key === 'maxAttemptsPerDay' ? 'Max Attempts/Day' : 'Max Copies/Doc'}:
                        </span>
                        <span className="ppt-change-values">
                          {change.current} → {change.proposed}
                        </span>
                      </div>
                    ))}
                  </div>
                  <div className="ppt-proposal-justification">
                    <strong>Justification:</strong> {proposal.justification}
                  </div>
                  {proposal.vcDecision && (
                    <div className={`ppt-vc-decision ${proposal.status}`}>
                      <strong>VC Decision:</strong> {proposal.vcDecision.notes}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Special User Policies Section */}
      {activeSection === 'special' && (
        <div className="ppt-section ppt-special-section">
          <div className="ppt-two-column">
            {/* Left: Search & Form */}
            <div className="ppt-special-form">
              <h3>🔍 Search User by EPF</h3>
              
              {specialMessage && (
                <div className={`ppt-message ${specialMessage.type}`}>
                  {specialMessage.text}
                </div>
              )}

              <div className="ppt-epf-search">
                <input
                  type="text"
                  placeholder="Enter EPF number..."
                  value={searchEpf}
                  onChange={(e) => setSearchEpf(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearchUser()}
                />
                <button 
                  onClick={handleSearchUser} 
                  className="ppt-btn primary"
                  disabled={searchLoading}
                >
                  {searchLoading ? '⏳' : '🔍'} Search
                </button>
              </div>

              {selectedUser && (
                <>
                  <div className="ppt-user-info">
                    <h4>👤 Selected User</h4>
                    <div className="ppt-user-details">
                      <div><strong>EPF:</strong> {selectedUser.epf}</div>
                      <div><strong>Name:</strong> {selectedUser.name}</div>
                      <div><strong>Department:</strong> {selectedUser.department}</div>
                      <div><strong>Role:</strong> {selectedUser.role}</div>
                    </div>
                  </div>

                  <form onSubmit={handleSubmitSpecialProposal}>
                    <h4>⚙️ Special Policy Limits</h4>
                    
                    <div className="ppt-form-row">
                      <label>Max Print Attempts per Day</label>
                      <div className="ppt-comparison">
                        <input
                          type="number"
                          min="1"
                          max="100"
                          value={specialPolicies.maxAttemptsPerDay}
                          onChange={(e) => setSpecialPolicies(prev => ({
                            ...prev,
                            maxAttemptsPerDay: parseInt(e.target.value)
                          }))}
                          className={specialPolicies.maxAttemptsPerDay !== currentPolicies.maxAttemptsPerDay ? 'changed' : ''}
                        />
                        <span className="ppt-change-indicator">
                          Global: {currentPolicies.maxAttemptsPerDay} → Special: {specialPolicies.maxAttemptsPerDay}
                        </span>
                      </div>
                    </div>

                    <div className="ppt-form-row">
                      <label>Max Copies per Document</label>
                      <div className="ppt-comparison">
                        <input
                          type="number"
                          min="1"
                          max="100"
                          value={specialPolicies.maxCopiesPerDoc}
                          onChange={(e) => setSpecialPolicies(prev => ({
                            ...prev,
                            maxCopiesPerDoc: parseInt(e.target.value)
                          }))}
                          className={specialPolicies.maxCopiesPerDoc !== currentPolicies.maxCopiesPerDoc ? 'changed' : ''}
                        />
                        <span className="ppt-change-indicator">
                          Global: {currentPolicies.maxCopiesPerDoc} → Special: {specialPolicies.maxCopiesPerDoc}
                        </span>
                      </div>
                    </div>

                    <div className="ppt-form-row">
                      <label>Justification *</label>
                      <textarea
                        value={specialJustification}
                        onChange={(e) => setSpecialJustification(e.target.value)}
                        placeholder="Explain why this user needs special limits..."
                        rows={4}
                        required
                      />
                    </div>

                    <div className="ppt-form-actions">
                      <button type="submit" className="ppt-btn primary" disabled={specialLoading}>
                        {specialLoading ? '⏳ Submitting...' : '📤 Submit for VC Approval'}
                      </button>
                      <button 
                        type="button" 
                        className="ppt-btn secondary"
                        onClick={() => {
                          setSelectedUser(null)
                          setSearchEpf('')
                          setSpecialPolicies(currentPolicies)
                          setSpecialJustification('')
                          setSpecialMessage(null)
                        }}
                        disabled={specialLoading}
                      >
                        ✖️ Clear
                      </button>
                    </div>
                  </form>
                </>
              )}
            </div>

            {/* Right: Special Proposals List */}
            <div className="ppt-special-proposals">
              <h3>📋 Special User Proposals</h3>
              {specialProposals.length === 0 ? (
                <div className="ppt-empty-state">No special user proposals yet</div>
              ) : (
                specialProposals.map(proposal => (
                  <div key={proposal.id} className={`ppt-proposal-card ${proposal.status}`}>
                    <div className="ppt-proposal-header">
                      <span className={`ppt-status-badge ${proposal.status}`}>
                        {proposal.status === 'pending' && '⏳ Pending'}
                        {proposal.status === 'approved' && '✅ Approved'}
                        {proposal.status === 'rejected' && '❌ Rejected'}
                      </span>
                      <span className="ppt-proposal-date">{formatDate(proposal.submittedAt)}</span>
                    </div>
                    <div className="ppt-user-info-compact">
                      <strong>User:</strong> {proposal.targetName} (EPF: {proposal.targetEPF})<br />
                      <strong>Dept:</strong> {proposal.targetDept}
                    </div>
                    <div className="ppt-proposal-changes">
                      <div className="ppt-change-item">
                        <span className="ppt-change-label">Max Attempts/Day:</span>
                        <span className="ppt-change-values">{proposal.proposedPolicy.maxAttemptsPerDay}</span>
                      </div>
                      <div className="ppt-change-item">
                        <span className="ppt-change-label">Max Copies/Doc:</span>
                        <span className="ppt-change-values">{proposal.proposedPolicy.maxCopiesPerDoc}</span>
                      </div>
                    </div>
                    <div className="ppt-proposal-justification">
                      <strong>Justification:</strong> {proposal.justification}
                    </div>
                    {proposal.vcDecision && (
                      <div className={`ppt-vc-decision ${proposal.status}`}>
                        <strong>VC Decision:</strong> {proposal.vcDecision.notes}
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}

      {/* All Proposals Combined View */}
      {activeSection === 'all' && (
        <div className="ppt-section">
          <div className="ppt-filter-bar">
            <label>Filter by Status:</label>
            <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
              <option value="all">All</option>
              <option value="pending">Pending</option>
              <option value="approved">Approved</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>

          <div className="ppt-proposals-list">
            {allProposals.length === 0 ? (
              <div className="ppt-empty-state">No proposals found</div>
            ) : (
              allProposals.map(proposal => (
                <div key={proposal.id} className={`ppt-proposal-card ${proposal.status}`}>
                  <div className="ppt-proposal-header">
                    <span className={`ppt-type-badge ${proposal.type}`}>
                      {proposal.type === 'global' && '🌐 Global'}
                      {proposal.type === 'special_user' && '👤 Special User'}
                      {proposal.type === 'removal' && '🗑️ Removal'}
                    </span>
                    <span className={`ppt-status-badge ${proposal.status}`}>
                      {proposal.status === 'pending' && '⏳ Pending'}
                      {proposal.status === 'approved' && '✅ Approved'}
                      {proposal.status === 'rejected' && '❌ Rejected'}
                    </span>
                    <span className="ppt-proposal-date">{formatDate(proposal.submittedAt)}</span>
                  </div>

                  {(proposal.type === 'special_user' || proposal.type === 'removal') && (
                    <div className="ppt-user-info-compact">
                      <strong>User:</strong> {proposal.targetName} (EPF: {proposal.targetEPF})
                    </div>
                  )}

                  <div className="ppt-proposal-changes">
                    {proposal.type === 'global' ? (
                      Object.entries(proposal.changes).map(([key, change]) => (
                        <div key={key} className="ppt-change-item">
                          <span className="ppt-change-label">
                            {key === 'maxAttemptsPerDay' ? 'Max Attempts/Day' : 'Max Copies/Doc'}:
                          </span>
                          <span className="ppt-change-values">
                            {change.current} → {change.proposed}
                          </span>
                        </div>
                      ))
                    ) : proposal.type === 'removal' ? (
                      <div className="ppt-change-item" style={{ background: '#fee', padding: '12px', borderRadius: '6px' }}>
                        <span className="ppt-change-label" style={{ color: '#c00' }}>
                          ⚠️ Action: Remove special policy - user will revert to global limits
                        </span>
                      </div>
                    ) : (
                      <>
                        <div className="ppt-change-item">
                          <span className="ppt-change-label">Max Attempts/Day:</span>
                          <span className="ppt-change-values">{proposal.proposedPolicy.maxAttemptsPerDay}</span>
                        </div>
                        <div className="ppt-change-item">
                          <span className="ppt-change-label">Max Copies/Doc:</span>
                          <span className="ppt-change-values">{proposal.proposedPolicy.maxCopiesPerDoc}</span>
                        </div>
                      </>
                    )}
                  </div>

                  <div className="ppt-proposal-justification">
                    <strong>Justification:</strong> {proposal.justification}
                  </div>

                  {proposal.vcDecision && (
                    <div className={`ppt-vc-decision ${proposal.status}`}>
                      <strong>VC Decision:</strong> {proposal.vcDecision.notes}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  )
}
