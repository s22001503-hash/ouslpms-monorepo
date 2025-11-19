import React, { useState } from 'react'
import { useAuth } from '../hooks/useAuth'
import ChangePassword from '../components/ChangePassword'
import PrintWorkflow from '../components/PrintWorkflow'
import ClassificationBadge from '../components/ClassificationBadge'
import './UserDashboardUI.css'

export default function UserDashboardUI() {
  const { user, logout, userEpf } = useAuth()
  const [activeView, setActiveView] = useState('notifications') // 'notifications', 'previousJobs', 'printDocument', or 'changePassword'

  // Enhanced notifications with VC decisions
  const notifications = [
    { 
      id: 'VC001', 
      type: 'vc_approved',
      status: 'approved', 
      ts: '2024-11-12 09:15 AM',
      document: 'Research_Paper_Final.pdf',
      vcNotes: 'Approved for academic purposes. Please use duplex printing.'
    },
    { 
      id: 'VC002', 
      type: 'vc_rejected',
      status: 'rejected', 
      ts: '2024-11-11 03:30 PM',
      document: 'Class_Notes.pdf',
      vcNotes: 'Similar document was printed yesterday. Please reuse previous copies.'
    },
    { 
      id: 'PJ001', 
      type: 'print_failed',
      status: 'terminated', 
      ts: '2024-09-24 10:30 AM' 
    },
    { 
      id: 'PJ002', 
      type: 'print_failed',
      status: 'failed', 
      ts: '2024-09-23 02:15 PM' 
    },
  ]

  return (
    <div className="ud-root">
      <aside className="ud-sidebar">
        <div className="ud-brand">
          <img src="/OUSL LOGO.jpg" alt="OUSL" />
          <div className="ud-brand-text">EcoPrint</div>
        </div>

        <nav className="ud-nav">
          <button 
            className={`ud-nav-item ${activeView === 'notifications' ? 'active' : ''}`}
            onClick={() => setActiveView('notifications')}
          >
            🔔 Notifications
          </button>
          <button 
            className={`ud-nav-item ${activeView === 'printDocument' ? 'active' : ''}`}
            onClick={() => setActiveView('printDocument')}
          >
            🖨️ Print Document
          </button>
          <button 
            className={`ud-nav-item ${activeView === 'previousJobs' ? 'active' : ''}`}
            onClick={() => setActiveView('previousJobs')}
          >
            � Previous Jobs
          </button>
          <button 
            className={`ud-nav-item ${activeView === 'changePassword' ? 'active' : ''}`}
            onClick={() => setActiveView('changePassword')}
          >
            🔒 Change Password
          </button>
        </nav>

        <div className="ud-logout">
          <button className="ud-logout-btn" onClick={async () => { await logout(); window.location.href = '/login' }}>
            ➡️ Logout
          </button>
        </div>
      </aside>

      <main className="ud-content">
        <header className="ud-header">
          <h1>EcoPrint Smart Print Management System</h1>
        </header>

        {activeView === 'notifications' && (
          <>
            <section className="ud-welcome">
              <h2>Welcome to EcoPrint</h2>
              <p>Manage your print jobs and view notifications here.</p>
            </section>

            <section className="ud-notifications">
              <div className="ud-card">
                <div className="ud-card-header">🔔 Notifications</div>
                <div className="ud-card-body">
                  {notifications.length === 0 ? (
                    <p style={{ textAlign: 'center', color: '#666', padding: '20px' }}>
                      No notifications
                    </p>
                  ) : (
                    notifications.map(n => (
                      <div key={n.id} className={`ud-notif ud-notif-${n.type}`}>
                        {n.type === 'vc_approved' && (
                          <>
                            <div className="ud-notif-icon">✅</div>
                            <div className="ud-notif-content">
                              <div className="ud-notif-title">VC Approved Your Print Request</div>
                              <div className="ud-notif-document">Document: {n.document}</div>
                              {n.vcNotes && (
                                <div className="ud-notif-notes">
                                  <strong>VC Notes:</strong> {n.vcNotes}
                                </div>
                              )}
                              <div className="ud-notif-ts">{n.ts}</div>
                            </div>
                          </>
                        )}
                        {n.type === 'vc_rejected' && (
                          <>
                            <div className="ud-notif-icon">❌</div>
                            <div className="ud-notif-content">
                              <div className="ud-notif-title">VC Rejected Your Print Request</div>
                              <div className="ud-notif-document">Document: {n.document}</div>
                              {n.vcNotes && (
                                <div className="ud-notif-notes">
                                  <strong>Reason:</strong> {n.vcNotes}
                                </div>
                              )}
                              <div className="ud-notif-ts">{n.ts}</div>
                            </div>
                          </>
                        )}
                        {n.type === 'print_failed' && (
                          <>
                            <div className="ud-notif-icon">⚠️</div>
                            <div className="ud-notif-content">
                              <div className="ud-notif-id">Print job #{n.id}</div>
                              <div className="ud-notif-status">Status: <strong>{n.status}</strong></div>
                              <div className="ud-notif-ts">{n.ts}</div>
                            </div>
                          </>
                        )}
                      </div>
                    ))
                  )}
                </div>
              </div>
            </section>
          </>
        )}

        {activeView === 'previousJobs' && (
          <section className="ud-welcome">
            <h2>Previous Print Jobs</h2>
            <p>Your print job history will appear here.</p>
            <div className="ud-card" style={{ marginTop: '20px' }}>
              <div className="ud-card-body">
                <p style={{ textAlign: 'center', color: '#666', padding: '40px' }}>
                  No previous print jobs to display.
                </p>
              </div>
            </div>
          </section>
        )}

        {activeView === 'printDocument' && (
          <section className="ud-print-section">
            <h2>🖨️ Print Document</h2>
            <p style={{ marginBottom: '20px', color: '#64748b' }}>
              Upload a document to print with AI-powered classification
            </p>
            <PrintWorkflow userEpf={userEpf} userName={user?.displayName} />
          </section>
        )}

        {activeView === 'changePassword' && (
          <section className="ud-change-password">
            <div className="ud-card">
              <ChangePassword
                onSuccess={() => {
                  console.log('Password changed successfully!')
                  // Optionally redirect back to notifications
                  setTimeout(() => setActiveView('notifications'), 2000)
                }}
                onCancel={() => setActiveView('notifications')}
              />
            </div>
          </section>
        )}
      </main>
    </div>
  )
}
