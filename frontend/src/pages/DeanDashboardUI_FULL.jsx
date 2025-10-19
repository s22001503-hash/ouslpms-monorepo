import React, { useState, useEffect } from 'react'
import { useAuth } from '../hooks/useAuth'
import { 
  fetchDeanOverview, 
  fetchSettingsProposals, 
  approveSettingsProposal, 
  rejectSettingsProposal,
  fetchDeanNotifications,
  fetchDeanReports
} from '../services/api'
import ChangePassword from '../components/ChangePassword'
import OverviewTab from '../components/OverviewTab'
import './DeanDashboardUI.css'

export default function DeanDashboardUI() {
  const { user, logout } = useAuth()
  const [activeView, setActiveView] = useState('overview')
  const [overviewStats, setOverviewStats] = useState({
    todayPrintJobs: 0,
    pendingProposals: 0,
    blockedAttempts: 0,
    activeUsers: 0
  })
  const [proposals, setProposals] = useState([])
  const [notifications, setNotifications] = useState([])
  const [reports, setReports] = useState(null)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState({ type: '', text: '' })

  // Fetch overview stats on mount
  useEffect(() => {
    if (activeView === 'overview') {
      loadOverviewStats()
    } else if (activeView === 'settingsProposal') {
      loadProposals()
    } else if (activeView === 'notifications') {
      loadNotifications()
    } else if (activeView === 'reports') {
      loadReports()
    }
  }, [activeView])

  const loadOverviewStats = async () => {
    try {
      const data = await fetchDeanOverview()
      setOverviewStats(data)
    } catch (error) {
      console.error('Failed to fetch overview stats:', error)
      setOverviewStats({
        todayPrintJobs: 0,
        pendingProposals: 0,
        blockedAttempts: 0,
        activeUsers: 0
      })
    }
  }

  const loadProposals = async () => {
    setLoading(true)
    try {
      const data = await fetchSettingsProposals('pending')
      setProposals(data.proposals || [])
    } catch (error) {
      console.error('Failed to fetch proposals:', error)
      setMessage({ type: 'error', text: error.message || 'Failed to load proposals' })
    } finally {
      setLoading(false)
    }
  }

  const loadNotifications = async () => {
    setLoading(true)
    try {
      const data = await fetchDeanNotifications()
      setNotifications(data.notifications || [])
    } catch (error) {
      console.error('Failed to fetch notifications:', error)
      setMessage({ type: 'error', text: error.message || 'Failed to load notifications' })
    } finally {
      setLoading(false)
    }
  }

  const loadReports = async () => {
    setLoading(true)
    try {
      const data = await fetchDeanReports()
      setReports(data)
    } catch (error) {
      console.error('Failed to fetch reports:', error)
      setMessage({ type: 'error', text: error.message || 'Failed to load reports' })
    } finally {
      setLoading(false)
    }
  }

  const handleNavigate = (view) => {
    setActiveView(view)
    setMessage({ type: '', text: '' })
  }

  const handleApprove = async (proposalId, adminName) => {
    if (!confirm(`Approve settings proposal from ${adminName}?`)) return
    
    setLoading(true)
    setMessage({ type: '', text: '' })
    
    try {
      await approveSettingsProposal(proposalId, user.uid, user.displayName || 'Dean', '')
      setMessage({ type: 'success', text: 'Proposal approved successfully!' })
      // Reload proposals
      await loadProposals()
      // Reload overview stats
      await loadOverviewStats()
    } catch (error) {
      setMessage({ type: 'error', text: error.message || 'Failed to approve proposal' })
    } finally {
      setLoading(false)
    }
  }

  const handleReject = async (proposalId, adminName) => {
    const reason = prompt(`Enter reason for rejecting ${adminName}'s proposal (optional):`)
    if (reason === null) return // User cancelled
    
    setLoading(true)
    setMessage({ type: '', text: '' })
    
    try {
      await rejectSettingsProposal(proposalId, user.uid, user.displayName || 'Dean', reason)
      setMessage({ type: 'success', text: 'Proposal rejected' })
      // Reload proposals
      await loadProposals()
      // Reload overview stats
      await loadOverviewStats()
    } catch (error) {
      setMessage({ type: 'error', text: error.message || 'Failed to reject proposal' })
    } finally {
      setLoading(false)
    }
  }

  const exportReportCSV = () => {
    if (!reports) return
    
    // Create CSV content
    let csv = 'Report Type,Value\n'
    csv += `Total Print Jobs,${reports.totalPrintJobs}\n`
    csv += `Total Blocked Attempts,${reports.totalBlockedAttempts}\n`
    csv += `\nProposal Statistics\n`
    csv += `Total,${reports.proposalStats.total}\n`
    csv += `Pending,${reports.proposalStats.pending}\n`
    csv += `Approved,${reports.proposalStats.approved}\n`
    csv += `Rejected,${reports.proposalStats.rejected}\n`
    csv += `\nTop Users (User ID, Print Jobs)\n`
    reports.topUsers.forEach(u => {
      csv += `${u.userId},${u.printJobs}\n`
    })
    
    // Download CSV
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `dean-report-${new Date().toISOString().split('T')[0]}.csv`
    a.click()
    window.URL.revokeObjectURL(url)
  }

  return (
    <div className="ad-root">
      <aside className="ad-sidebar">
        <div className="ad-brand">
          <img src="/OUSL LOGO.jpg" alt="OUSL" />
          <div className="ad-brand-text">EcoPrint Dean</div>
        </div>

        <nav className="ad-nav">
          <button 
            className={`ad-nav-item ${activeView === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveView('overview')}
          >
            🏠 Overview
          </button>
          <button 
            className={`ad-nav-item ${activeView === 'notifications' ? 'active' : ''}`}
            onClick={() => setActiveView('notifications')}
          >
            🔔 Notifications
            {notifications.filter(n => !n.read).length > 0 && (
              <span className="ad-badge">{notifications.filter(n => !n.read).length}</span>
            )}
          </button>
          <button 
            className={`ad-nav-item ${activeView === 'reports' ? 'active' : ''}`}
            onClick={() => setActiveView('reports')}
          >
            📊 Generate Report
          </button>
          <button 
            className={`ad-nav-item ${activeView === 'changePassword' ? 'active' : ''}`}
            onClick={() => setActiveView('changePassword')}
          >
            🔒 Change Password
          </button>
        </nav>

        <div className="ad-logout">
          <button className="ad-logout-btn" onClick={async () => { await logout(); window.location.href = '/login' }}>
            ➡️ Logout
          </button>
        </div>
      </aside>

      <main className="ad-content">
        <header className="ad-header">
          <h1>Dean Dashboard - EcoPrint</h1>
        </header>

        <section className="ad-banner">
          <h2>Welcome, Dean</h2>
          <p>Review and approve system settings proposals and monitor overall system performance.</p>
        </section>

        {message.text && (
          <div className={`ad-message ${message.type}`}>
            {message.text}
          </div>
        )}

        <section className="ad-main">
          {/* Overview Tab */}
          {activeView === 'overview' && (
            <OverviewTab 
              stats={overviewStats} 
              onNavigate={handleNavigate}
              quickActions={[
                { icon: '⚙️', label: 'Review Proposals', view: 'settingsProposal' }
              ]}
            />
          )}

          {/* Settings Proposal Review Tab */}
          {activeView === 'settingsProposal' && (
            <div className="ad-card">
              <div className="ad-card-header">
                <h3>Review Settings Proposals</h3>
                <span className="ad-badge-info">{proposals.length} Pending</span>
              </div>
              <div className="ad-card-body">
                {loading ? (
                  <div style={{ padding: '40px', textAlign: 'center' }}>
                    <p>Loading proposals...</p>
                  </div>
                ) : proposals.length === 0 ? (
                  <div style={{ padding: '40px', textAlign: 'center', color: '#666' }}>
                    <p>✅ No pending proposals to review</p>
                  </div>
                ) : (
                  <div className="proposals-list">
                    {proposals.map((proposal) => (
                      <div key={proposal.id} className="proposal-item">
                        <div className="proposal-header">
                          <div>
                            <h4>Proposal from {proposal.adminName || 'Admin'}</h4>
                            <p className="proposal-email">{proposal.adminEmail}</p>
                            <p className="proposal-time">
                              Submitted: {new Date(proposal.submittedAt).toLocaleString()}
                            </p>
                          </div>
                          <div className="proposal-actions">
                            <button 
                              className="btn-approve"
                              onClick={() => handleApprove(proposal.id, proposal.adminName)}
                              disabled={loading}
                            >
                              ✅ Approve
                            </button>
                            <button 
                              className="btn-reject"
                              onClick={() => handleReject(proposal.id, proposal.adminName)}
                              disabled={loading}
                            >
                              ❌ Reject
                            </button>
                          </div>
                        </div>
                        
                        <div className="proposal-settings">
                          <h5>Proposed Settings:</h5>
                          <table className="settings-table">
                            <thead>
                              <tr>
                                <th>Setting</th>
                                <th>Current Value</th>
                                <th>Proposed Value</th>
                              </tr>
                            </thead>
                            <tbody>
                              {Object.entries(proposal.proposedSettings).map(([key, value]) => (
                                <tr key={key}>
                                  <td>{key.replace(/([A-Z])/g, ' $1').trim()}</td>
                                  <td>{String(proposal.currentSettings?.[key] ?? 'N/A')}</td>
                                  <td className="proposed-value">{String(value)}</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Notifications Tab */}
          {activeView === 'notifications' && (
            <div className="ad-card">
              <div className="ad-card-header">
                <h3>Notifications</h3>
                <span className="ad-badge-info">
                  {notifications.filter(n => !n.read).length} Unread
                </span>
              </div>
              <div className="ad-card-body">
                {loading ? (
                  <div style={{ padding: '40px', textAlign: 'center' }}>
                    <p>Loading notifications...</p>
                  </div>
                ) : notifications.length === 0 ? (
                  <div style={{ padding: '40px', textAlign: 'center', color: '#666' }}>
                    <p>No notifications</p>
                  </div>
                ) : (
                  <div className="notifications-list">
                    {notifications.map((notif) => (
                      <div key={notif.id} className={`notification-item ${notif.priority}`}>
                        <div className="notif-icon">
                          {notif.type === 'proposal' ? '⚙️' : '🚫'}
                        </div>
                        <div className="notif-content">
                          <h4>{notif.title}</h4>
                          <p>{notif.message}</p>
                          <span className="notif-time">
                            {new Date(notif.timestamp).toLocaleString()}
                          </span>
                        </div>
                        <div className="notif-badge">
                          {!notif.read && <span className="unread-dot"></span>}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Generate Report Tab */}
          {activeView === 'reports' && (
            <div className="ad-card">
              <div className="ad-card-header">
                <h3>System Oversight Reports</h3>
                {reports && (
                  <button className="btn-export" onClick={exportReportCSV}>
                    📥 Export CSV
                  </button>
                )}
              </div>
              <div className="ad-card-body">
                {loading ? (
                  <div style={{ padding: '40px', textAlign: 'center' }}>
                    <p>Generating reports...</p>
                  </div>
                ) : !reports ? (
                  <div style={{ padding: '40px', textAlign: 'center', color: '#666' }}>
                    <p>Report generation failed. Please try again.</p>
                  </div>
                ) : (
                  <div className="reports-container">
                    <div className="report-section">
                      <h4>Summary Statistics</h4>
                      <div className="report-stats">
                        <div className="stat-box">
                          <span className="stat-label">Total Print Jobs (30 days)</span>
                          <span className="stat-value">{reports.totalPrintJobs}</span>
                        </div>
                        <div className="stat-box">
                          <span className="stat-label">Total Blocked Attempts (7 days)</span>
                          <span className="stat-value">{reports.totalBlockedAttempts}</span>
                        </div>
                      </div>
                    </div>

                    <div className="report-section">
                      <h4>Proposal Statistics</h4>
                      <table className="report-table">
                        <tbody>
                          <tr>
                            <td>Total Proposals</td>
                            <td>{reports.proposalStats.total}</td>
                          </tr>
                          <tr>
                            <td>Pending</td>
                            <td className="pending">{reports.proposalStats.pending}</td>
                          </tr>
                          <tr>
                            <td>Approved</td>
                            <td className="approved">{reports.proposalStats.approved}</td>
                          </tr>
                          <tr>
                            <td>Rejected</td>
                            <td className="rejected">{reports.proposalStats.rejected}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>

                    <div className="report-section">
                      <h4>Top Users by Print Jobs (Last 30 Days)</h4>
                      <table className="report-table">
                        <thead>
                          <tr>
                            <th>Rank</th>
                            <th>User ID</th>
                            <th>Print Jobs</th>
                          </tr>
                        </thead>
                        <tbody>
                          {reports.topUsers.map((user, idx) => (
                            <tr key={user.userId}>
                              <td>{idx + 1}</td>
                              <td>{user.userId}</td>
                              <td>{user.printJobs}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>

                    <div className="report-section">
                      <h4>Blocked Attempts by Day (Last 7 Days)</h4>
                      <table className="report-table">
                        <thead>
                          <tr>
                            <th>Date</th>
                            <th>Blocked Attempts</th>
                          </tr>
                        </thead>
                        <tbody>
                          {Object.entries(reports.blockedAttemptsByDay)
                            .sort((a, b) => b[0].localeCompare(a[0]))
                            .map(([date, count]) => (
                              <tr key={date}>
                                <td>{date}</td>
                                <td>{count}</td>
                              </tr>
                            ))}
                        </tbody>
                      </table>
                    </div>

                    <div className="report-footer">
                      <p>Report generated: {new Date(reports.reportGenerated).toLocaleString()}</p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Change Password Tab */}
          {activeView === 'changePassword' && (
            <div className="ad-card">
              <ChangePassword
                onSuccess={() => {
                  console.log('Password changed successfully')
                  setMessage({ type: 'success', text: 'Password changed successfully!' })
                }}
                onCancel={() => setActiveView('overview')}
              />
            </div>
          )}
        </section>
      </main>
    </div>
  )
}
