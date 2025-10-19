import React, { useState, useEffect } from 'react'
import { useAuth } from '../hooks/useAuth'
import { fetchOverviewStats as fetchOverviewStatsAPI } from '../services/api'
import ChangePassword from '../components/ChangePassword'
import OverviewTab from '../components/OverviewTab'
import './DeanDashboardUI.css'

export default function DeanDashboardUI() {
  const { user, logout } = useAuth()
  const [activeView, setActiveView] = useState('overview') // 'overview', 'settingsProposal', 'changePassword'
  const [overviewStats, setOverviewStats] = useState({
    todayPrintJobs: 0,
    pendingProposals: 0,
    blockedAttempts: 0,
    activeUsers: 0,
    recentActivity: []
  })

  // Fetch overview stats on mount
  useEffect(() => {
    if (activeView === 'overview') {
      loadOverviewStats()
    }
  }, [activeView])

  const loadOverviewStats = async () => {
    try {
      const data = await fetchOverviewStatsAPI()
      setOverviewStats(data)
    } catch (error) {
      console.error('Failed to fetch overview stats:', error)
      // Fallback to mock data if API fails
      setOverviewStats({
        todayPrintJobs: 0,
        pendingProposals: 0,
        blockedAttempts: 0,
        activeUsers: 0,
        recentActivity: []
      })
    }
  }

  const handleNavigate = (view) => {
    setActiveView(view)
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
          <button className="ad-nav-item">🔔 Notifications</button>
          <button className="ad-nav-item">📊 Generate Report</button>
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

        <section className="ad-main">
          {activeView === 'overview' && (
            <OverviewTab 
              stats={overviewStats} 
              onNavigate={handleNavigate}
              quickActions={[
                { icon: '⚙️', label: 'Review Proposals', view: 'settingsProposal' }
              ]}
            />
          )}

          {activeView === 'settingsProposal' && (
            <div className="ad-card">
              <div className="ad-card-header">Review Settings Proposals</div>
              <div className="ad-card-body">
                <p style={{ padding: '40px', textAlign: 'center', color: '#666' }}>
                  Settings proposal review interface coming soon...
                  <br /><br />
                  This will display pending proposals from admins for your review and approval.
                </p>
              </div>
            </div>
          )}

          {activeView === 'changePassword' && (
            <div className="ad-card">
              <ChangePassword
                onSuccess={() => {
                  console.log('Password changed successfully')
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
