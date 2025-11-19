import React, { useState, useEffect } from 'react'
import './SpecialUsersManagementTab.css'
import { requestRemovalProposal } from '../services/api'

/**
 * SpecialUsersManagementTab - Manage users with active special policies
 * Features:
 * - Grid view of all users with special policies
 * - Search and filter functionality
 * - Remove special policy from users
 * - View policy details and usage statistics
 */
export default function SpecialUsersManagementTab({ adminId }) {
  const [specialUsers, setSpecialUsers] = useState([])
  const [filteredUsers, setFilteredUsers] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const [filterDepartment, setFilterDepartment] = useState('all')
  const [loading, setLoading] = useState(true)
  const [message, setMessage] = useState(null)
  const [selectedUser, setSelectedUser] = useState(null)
  const [showConfirmDialog, setShowConfirmDialog] = useState(false)
  const [removing, setRemoving] = useState(false)
  const [removalJustification, setRemovalJustification] = useState('')

  useEffect(() => {
    loadSpecialUsers()
  }, [])

  useEffect(() => {
    filterUsers()
  }, [searchQuery, filterDepartment, specialUsers])

  const loadSpecialUsers = async () => {
    setLoading(true)
    try {
      // TODO: Replace with actual API call
      // const users = await getSpecialPolicyUsers()
      
      // Mock data
      const mockUsers = [
        {
          epf: '60025',
          name: 'Maria Research',
          email: 'maria.research@ousl.lk',
          department: 'Computer Science',
          role: 'user',
          specialPolicy: {
            maxAttemptsPerDay: 15,
            maxCopiesPerDoc: 20,
            approvedAt: '2025-11-10T16:00:00Z',
            approvedBy: 'VC Dr. Smith',
            justification: 'Research assistant needs higher limits for daily research paper printing.'
          },
          usage: {
            totalPrints: 142,
            averageDaily: 8,
            lastPrint: '2025-11-12T10:30:00Z'
          }
        },
        {
          epf: '60089',
          name: 'John Professor',
          email: 'john.prof@ousl.lk',
          department: 'Engineering',
          role: 'user',
          specialPolicy: {
            maxAttemptsPerDay: 20,
            maxCopiesPerDoc: 25,
            approvedAt: '2025-11-08T14:00:00Z',
            approvedBy: 'VC Dr. Smith',
            justification: 'Professor needs higher limits for course material distribution.'
          },
          usage: {
            totalPrints: 256,
            averageDaily: 12,
            lastPrint: '2025-11-12T09:15:00Z'
          }
        },
        {
          epf: '60134',
          name: 'Sarah Lab',
          email: 'sarah.lab@ousl.lk',
          department: 'Computer Science',
          role: 'user',
          specialPolicy: {
            maxAttemptsPerDay: 10,
            maxCopiesPerDoc: 15,
            approvedAt: '2025-11-09T11:30:00Z',
            approvedBy: 'VC Dr. Smith',
            justification: 'Lab coordinator needs extra prints for practical sessions.'
          },
          usage: {
            totalPrints: 89,
            averageDaily: 5,
            lastPrint: '2025-11-11T15:45:00Z'
          }
        }
      ]
      
      setSpecialUsers(mockUsers)
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to load special users' })
    } finally {
      setLoading(false)
    }
  }

  const filterUsers = () => {
    let filtered = [...specialUsers]

    // Apply search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(user => 
        user.name.toLowerCase().includes(query) ||
        user.epf.includes(query) ||
        user.email.toLowerCase().includes(query) ||
        user.department.toLowerCase().includes(query)
      )
    }

    // Apply department filter
    if (filterDepartment !== 'all') {
      filtered = filtered.filter(user => user.department === filterDepartment)
    }

    setFilteredUsers(filtered)
  }

  const handleRemovePolicy = (user) => {
    setSelectedUser(user)
    setShowConfirmDialog(true)
  }

  const confirmRemovePolicy = async () => {
    if (!selectedUser) return

    setRemoving(true)
    try {
      await requestRemovalProposal(selectedUser.epf, adminId, removalJustification)
      
      setMessage({ 
        type: 'success', 
        text: `Removal request submitted for ${selectedUser.name}. Awaiting VC approval.` 
      })
      
      setShowConfirmDialog(false)
      setSelectedUser(null)
      setRemovalJustification('')
    } catch (error) {
      setMessage({ type: 'error', text: error.message || 'Failed to submit removal request' })
    } finally {
      setRemoving(false)
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

  const departments = ['all', ...new Set(specialUsers.map(u => u.department))]

  return (
    <div className="special-users-management-tab">
      <div className="sumt-header">
        <div className="sumt-title">
          <h2>⭐ Special Policy Users</h2>
          <p>Manage users with custom policy limits</p>
        </div>
        <div className="sumt-stats">
          <div className="sumt-stat-card">
            <span className="sumt-stat-value">{specialUsers.length}</span>
            <span className="sumt-stat-label">Active Special Policies</span>
          </div>
        </div>
      </div>

      {message && (
        <div className={`sumt-message ${message.type}`}>
          {message.text}
          <button 
            className="sumt-message-close"
            onClick={() => setMessage(null)}
          >
            ×
          </button>
        </div>
      )}

      {/* Search and Filter Bar */}
      <div className="sumt-controls">
        <div className="sumt-search">
          <input
            type="text"
            placeholder="🔍 Search by name, EPF, email, or department..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <div className="sumt-filter">
          <label>Department:</label>
          <select 
            value={filterDepartment} 
            onChange={(e) => setFilterDepartment(e.target.value)}
          >
            {departments.map(dept => (
              <option key={dept} value={dept}>
                {dept === 'all' ? 'All Departments' : dept}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Users Grid */}
      {loading ? (
        <div className="sumt-loading">⏳ Loading special users...</div>
      ) : filteredUsers.length === 0 ? (
        <div className="sumt-empty">
          {searchQuery || filterDepartment !== 'all' 
            ? '🔍 No users found matching your filters' 
            : '📋 No users with special policies yet'}
        </div>
      ) : (
        <div className="sumt-grid">
          {filteredUsers.map(user => (
            <div key={user.epf} className="sumt-user-card">
              {/* User Info Header */}
              <div className="sumt-card-header">
                <div className="sumt-user-info">
                  <h3>{user.name}</h3>
                  <p className="sumt-epf">EPF: {user.epf}</p>
                  <p className="sumt-department">{user.department}</p>
                </div>
                <button
                  className="sumt-remove-btn"
                  onClick={() => handleRemovePolicy(user)}
                  title="Request removal of special policy"
                >
                  📝
                </button>
              </div>

              {/* Policy Limits */}
              <div className="sumt-policy-section">
                <h4>📋 Special Policy Limits</h4>
                <div className="sumt-policy-grid">
                  <div className="sumt-policy-item">
                    <span className="sumt-policy-label">Max Attempts/Day:</span>
                    <span className="sumt-policy-value">{user.specialPolicy.maxAttemptsPerDay}</span>
                  </div>
                  <div className="sumt-policy-item">
                    <span className="sumt-policy-label">Max Copies/Doc:</span>
                    <span className="sumt-policy-value">{user.specialPolicy.maxCopiesPerDoc}</span>
                  </div>
                </div>
              </div>

              {/* Usage Statistics */}
              <div className="sumt-usage-section">
                <h4>📊 Usage Statistics</h4>
                <div className="sumt-usage-grid">
                  <div className="sumt-usage-item">
                    <span className="sumt-usage-label">Total Prints:</span>
                    <span className="sumt-usage-value">{user.usage.totalPrints}</span>
                  </div>
                  <div className="sumt-usage-item">
                    <span className="sumt-usage-label">Avg. Daily:</span>
                    <span className="sumt-usage-value">{user.usage.averageDaily}</span>
                  </div>
                </div>
                <div className="sumt-last-print">
                  Last print: {formatDate(user.usage.lastPrint)}
                </div>
              </div>

              {/* Approval Info */}
              <div className="sumt-approval-section">
                <h4>✅ Approval Details</h4>
                <p className="sumt-approval-date">
                  Approved on {formatDate(user.specialPolicy.approvedAt)}
                </p>
                <p className="sumt-approval-by">
                  By: {user.specialPolicy.approvedBy}
                </p>
                <p className="sumt-justification">
                  <strong>Reason:</strong> {user.specialPolicy.justification}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Confirmation Dialog */}
      {showConfirmDialog && (
        <div className="sumt-dialog-overlay">
          <div className="sumt-dialog">
            <div className="sumt-dialog-header">
              <h3>📝 Request Special Policy Removal</h3>
            </div>
            <div className="sumt-dialog-body">
              <p>Submit a removal request for:</p>
              <div className="sumt-dialog-user-info">
                <strong>{selectedUser?.name}</strong>
                <span>EPF: {selectedUser?.epf}</span>
                <span>{selectedUser?.department}</span>
              </div>
              <div style={{ marginTop: '16px' }}>
                <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
                  Justification for Removal: *
                </label>
                <textarea
                  value={removalJustification}
                  onChange={(e) => setRemovalJustification(e.target.value)}
                  placeholder="Explain why this special policy should be removed..."
                  rows={4}
                  style={{
                    width: '100%',
                    padding: '10px',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    fontSize: '14px',
                    fontFamily: 'inherit',
                    resize: 'vertical'
                  }}
                  required
                />
              </div>
              <p className="sumt-dialog-warning" style={{ marginTop: '12px' }}>
                ⚠️ This request will be sent to the VC for approval. Once approved, the user will revert to global policy limits.
              </p>
            </div>
            <div className="sumt-dialog-actions">
              <button
                className="sumt-btn secondary"
                onClick={() => {
                  setShowConfirmDialog(false)
                  setSelectedUser(null)
                  setRemovalJustification('')
                }}
                disabled={removing}
              >
                Cancel
              </button>
              <button
                className="sumt-btn danger"
                onClick={confirmRemovePolicy}
                disabled={removing || !removalJustification.trim()}
              >
                {removing ? '⏳ Submitting...' : '📤 Submit Request'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
