import React, { useState, useEffect } from 'react'
import { useAuth } from '../hooks/useAuth'
import { fetchOverviewStats as fetchOverviewStatsAPI } from '../services/api'
import ChangePassword from '../components/ChangePassword'
import OverviewTab from '../components/OverviewTab'
import ApprovalRequestsTab from '../components/ApprovalRequestsTab'
import PolicyManagementTab from '../components/PolicyManagementTab'
import './DeanDashboardUI.css'

export default function DeanDashboardUI() {
  const { user, logout } = useAuth()
  const [activeView, setActiveView] = useState('overview') // 'overview', 'approvalRequests', 'policyManagement', 'printDocument', 'changePassword'
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
          <div className="ad-brand-text">EcoPrint HOD</div>
        </div>

        <nav className="ad-nav">
          <button 
            className={`ad-nav-item ${activeView === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveView('overview')}
          >
            🏠 Overview
          </button>
          <button 
            className={`ad-nav-item ${activeView === 'approvalRequests' ? 'active' : ''}`}
            onClick={() => setActiveView('approvalRequests')}
          >
            📋 Approval Requests
          </button>
          <button 
            className={`ad-nav-item ${activeView === 'policyManagement' ? 'active' : ''}`}
            onClick={() => setActiveView('policyManagement')}
          >
            ⚙️ Policy Management
          </button>
          <button 
            className={`ad-nav-item ${activeView === 'printDocument' ? 'active' : ''}`}
            onClick={() => setActiveView('printDocument')}
          >
            🖨️ Print Document
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
          <h1>HOD Dashboard - EcoPrint</h1>
        </header>

        <section className="ad-banner">
          <h2>Welcome, HOD</h2>
          <p>Review and approve system settings proposals and monitor overall system performance.</p>
        </section>

        <section className="ad-main">
          {activeView === 'overview' && (
            <OverviewTab 
              stats={overviewStats}
              role="vc"
            />
          )}

          {activeView === 'approvalRequests' && (
            <div className="ad-card">
              <ApprovalRequestsTab vcId={user?.epf} />
            </div>
          )}

          {activeView === 'policyManagement' && (
            <div className="ad-card">
              <PolicyManagementTab vcId={user?.epf} />
            </div>
          )}

          {activeView === 'printDocument' && (
            <div className="ad-card">
              <div className="ad-card-header">🖨️ Print Document</div>
              <div className="ad-card-body">
                <div style={{ padding: '20px', textAlign: 'center' }}>
                  <div style={{ 
                    border: '2px dashed #ddd', 
                    borderRadius: '8px', 
                    padding: '40px', 
                    marginBottom: '20px',
                    background: '#f9f9f9'
                  }}>
                    <div style={{ fontSize: '48px', marginBottom: '16px' }}>📄</div>
                    <p style={{ color: '#666', marginBottom: '16px' }}>
                      Drag and drop your document here, or click to browse
                    </p>
                    <input 
                      type="file" 
                      accept=".pdf,.doc,.docx,.txt" 
                      style={{ display: 'none' }} 
                      id="hod-file-upload"
                    />
                    <label 
                      htmlFor="hod-file-upload" 
                      style={{
                        background: 'linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%)',
                        color: 'white',
                        padding: '12px 24px',
                        borderRadius: '8px',
                        cursor: 'pointer',
                        display: 'inline-block',
                        fontWeight: 600,
                        transition: 'all 0.3s ease'
                      }}
                    >
                      Choose File
                    </label>
                  </div>
                  
                  <div style={{ 
                    background: '#e3f2fd', 
                    padding: '16px', 
                    borderRadius: '8px',
                    textAlign: 'left',
                    border: '1px solid #bbdefb'
                  }}>
                    <h4 style={{ margin: '0 0 12px 0', color: '#1976d2' }}>
                      ℹ️ HOD Print Workflow:
                    </h4>
                    <ol style={{ margin: 0, paddingLeft: '20px', color: '#555' }}>
                      <li>Upload your document (PDF, DOC, DOCX, TXT)</li>
                      <li>AI classifies as Official, Personal, or Confidential</li>
                      <li>System checks HOD policy (20 pages/day, 20 copies, NO personal)</li>
                      <li>Review classification and confirm print</li>
                    </ol>
                  </div>
                  
                  <div style={{
                    marginTop: '20px',
                    padding: '12px',
                    background: '#fff3e0',
                    borderRadius: '8px',
                    border: '1px solid #ffe0b2'
                  }}>
                    <p style={{ margin: 0, fontSize: '14px', color: '#e65100' }}>
                      ⚡ <strong>HOD Privilege:</strong> Higher print limits (20 pages/day, 20 copies)
                    </p>
                  </div>
                  
                  <p style={{ 
                    marginTop: '20px', 
                    fontSize: '14px', 
                    color: '#666',
                    fontStyle: 'italic'
                  }}>
                    🚀 <strong>Coming Soon:</strong> AI classification with Pinecone + Groq + Modal.com
                  </p>
                </div>
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
