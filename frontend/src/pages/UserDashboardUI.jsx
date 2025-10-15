import React, { useState } from 'react'
import { useAuth } from '../hooks/useAuth'
import ChangePassword from '../components/ChangePassword'
import './UserDashboardUI.css'

export default function UserDashboardUI() {
  const { user, logout, userEpf } = useAuth()
  const [activeView, setActiveView] = useState('notifications') // 'notifications', 'previousJobs', or 'changePassword'

  // Sample notifications (would come from backend in real app)
  const notifications = [
    { id: 'PJ001', status: 'terminated', ts: '2024-09-24 10:30 AM' },
    { id: 'PJ002', status: 'failed', ts: '2024-09-23 02:15 PM' },
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
            className={`ud-nav-item ${activeView === 'previousJobs' ? 'active' : ''}`}
            onClick={() => setActiveView('previousJobs')}
          >
            🖨️ Previous Jobs
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
                <div className="ud-card-header">⚠️ Notifications</div>
                <div className="ud-card-body">
                  {notifications.map(n => (
                    <div key={n.id} className="ud-notif">
                      <div className="ud-notif-id">Print job #{n.id}</div>
                      <div className="ud-notif-status">Status: <strong>{n.status}</strong></div>
                      <div className="ud-notif-ts">{n.ts}</div>
                    </div>
                  ))}
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
