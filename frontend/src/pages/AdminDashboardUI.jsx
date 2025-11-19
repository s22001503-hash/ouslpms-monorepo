import React, { useState, useEffect } from 'react'
import { useAuth } from '../hooks/useAuth'
import { fetchOverviewStats as fetchOverviewStatsAPI } from '../services/api'
import ChangePassword from '../components/ChangePassword'
import OverviewTab from '../components/OverviewTab'
import SettingsProposalTab from '../components/SettingsProposalTab'
import PolicyProposalTab from '../components/PolicyProposalTab'
import UserManagementTab from '../components/UserManagementTab'
import SpecialUsersManagementTab from '../components/SpecialUsersManagementTab'
import './AdminDashboardUI.css'

export default function AdminDashboardUI() {
  const { user, logout } = useAuth()
  const [activeView, setActiveView] = useState('overview') // 'overview', 'userManagement', 'settingsProposal', 'policyProposal', 'generateReport', or 'changePassword'
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

  return (
    <div className="ad-root">
      <aside className="ad-sidebar">
        <div className="ad-brand">
          <img src="/OUSL LOGO.jpg" alt="OUSL" />
          <div className="ad-brand-text">EcoPrint Admin</div>
        </div>

        <nav className="ad-nav">
          <button 
            className={`ad-nav-item ${activeView === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveView('overview')}
          >
            🏠 Overview
          </button>
          <button 
            className={`ad-nav-item ${activeView === 'userManagement' ? 'active' : ''}`}
            onClick={() => setActiveView('userManagement')}
          >
            👥 User Management
          </button>
          <button 
            className={`ad-nav-item ${activeView === 'policyProposal' ? 'active' : ''}`}
            onClick={() => setActiveView('policyProposal')}
          >
            📝 Policy Proposals
          </button>
          <button 
            className={`ad-nav-item ${activeView === 'specialUsers' ? 'active' : ''}`}
            onClick={() => setActiveView('specialUsers')}
          >
            ⭐ Special Users
          </button>
          <button 
            className={`ad-nav-item ${activeView === 'printDocument' ? 'active' : ''}`}
            onClick={() => setActiveView('printDocument')}
          >
            🖨️ Print Document
          </button>
          <button className="ad-nav-item">🔔 Notifications</button>
          <button 
            className={`ad-nav-item ${activeView === 'generateReport' ? 'active' : ''}`}
            onClick={() => setActiveView('generateReport')}
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
          <h1>Admin Dashboard - EcoPrint</h1>
        </header>

        <section className="ad-banner">
          <h2>Welcome, Administrator</h2>
          <p>Use this panel to manage users, view reports, and handle notifications.</p>
        </section>

        <section className="ad-main">
          {activeView === 'overview' && (
            <OverviewTab 
              stats={overviewStats}
              role="admin"
            />
          )}

          {activeView === 'userManagement' && (
            <div className="ad-card">
              <UserManagementTab />
            </div>
          )}

          {activeView === 'settingsProposal' && (
            <SettingsProposalTab adminId={user?.epf} />
          )}

          {activeView === 'policyProposal' && (
            <div className="ad-card">
              <PolicyProposalTab adminId={user?.epf} />
            </div>
          )}

          {activeView === 'specialUsers' && (
            <div className="ad-card">
              <SpecialUsersManagementTab adminId={user?.epf} />
            </div>
          )}

          {activeView === 'generateReport' && (
            <div className="ad-card">
              <div className="ad-card-header">📊 Generate Report</div>
              <div className="ad-card-body">
                <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
                  <h3 style={{ marginBottom: '24px', color: '#2d3748' }}>System Reports</h3>
                  
                  <div style={{ display: 'grid', gap: '20px' }}>
                    {/* Print Activity Report */}
                    <div style={{ 
                      border: '1px solid #e2e8f0', 
                      borderRadius: '8px', 
                      padding: '20px',
                      background: '#fff'
                    }}>
                      <h4 style={{ margin: '0 0 12px 0', color: '#228B22' }}>📈 Print Activity Report</h4>
                      <p style={{ color: '#666', marginBottom: '16px', fontSize: '14px' }}>
                        Generate detailed report of all print jobs, classifications, and user activity
                      </p>
                      <div style={{ display: 'flex', gap: '12px', marginBottom: '12px' }}>
                        <input type="date" style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }} />
                        <span style={{ alignSelf: 'center' }}>📅 to</span>
                        <input type="date" style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }} />
                      </div>
                      <button style={{
                        background: 'linear-gradient(135deg, #228B22 0%, #1a6b1a 100%)',
                        color: 'white',
                        padding: '10px 20px',
                        borderRadius: '6px',
                        border: 'none',
                        cursor: 'pointer',
                        fontWeight: 600
                      }}>
                        📥 Generate CSV
                      </button>
                    </div>

                    {/* Block Reasons Report */}
                    <div style={{ 
                      border: '1px solid #e2e8f0', 
                      borderRadius: '8px', 
                      padding: '20px',
                      background: '#fff'
                    }}>
                      <h4 style={{ margin: '0 0 12px 0', color: '#228B22' }}>🚫 Block Reasons Report</h4>
                      <p style={{ color: '#666', marginBottom: '16px', fontSize: '14px' }}>
                        Export report of blocked print attempts and reasons
                      </p>
                      <div style={{ display: 'flex', gap: '12px', marginBottom: '12px' }}>
                        <input type="date" style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }} />
                        <span style={{ alignSelf: 'center' }}>📅 to</span>
                        <input type="date" style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }} />
                      </div>
                      <button style={{
                        background: 'linear-gradient(135deg, #228B22 0%, #1a6b1a 100%)',
                        color: 'white',
                        padding: '10px 20px',
                        borderRadius: '6px',
                        border: 'none',
                        cursor: 'pointer',
                        fontWeight: 600
                      }}>
                        📥 Generate CSV
                      </button>
                    </div>

                    {/* User Activity Report */}
                    <div style={{ 
                      border: '1px solid #e2e8f0', 
                      borderRadius: '8px', 
                      padding: '20px',
                      background: '#fff'
                    }}>
                      <h4 style={{ margin: '0 0 12px 0', color: '#228B22' }}>👥 User Activity Report</h4>
                      <p style={{ color: '#666', marginBottom: '16px', fontSize: '14px' }}>
                        Export detailed user-wise print statistics
                      </p>
                      <div style={{ display: 'flex', gap: '12px', marginBottom: '12px' }}>
                        <input type="date" style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }} />
                        <span style={{ alignSelf: 'center' }}>📅 to</span>
                        <input type="date" style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }} />
                      </div>
                      <button style={{
                        background: 'linear-gradient(135deg, #228B22 0%, #1a6b1a 100%)',
                        color: 'white',
                        padding: '10px 20px',
                        borderRadius: '6px',
                        border: 'none',
                        cursor: 'pointer',
                        fontWeight: 600
                      }}>
                        📥 Generate CSV
                      </button>
                    </div>

                    {/* Policy Proposals Report */}
                    <div style={{ 
                      border: '1px solid #e2e8f0', 
                      borderRadius: '8px', 
                      padding: '20px',
                      background: '#fff'
                    }}>
                      <h4 style={{ margin: '0 0 12px 0', color: '#228B22' }}>📋 Policy Proposals Report</h4>
                      <p style={{ color: '#666', marginBottom: '16px', fontSize: '14px' }}>
                        Export all policy proposals and their approval status
                      </p>
                      <button style={{
                        background: 'linear-gradient(135deg, #228B22 0%, #1a6b1a 100%)',
                        color: 'white',
                        padding: '10px 20px',
                        borderRadius: '6px',
                        border: 'none',
                        cursor: 'pointer',
                        fontWeight: 600
                      }}>
                        📥 Generate CSV
                      </button>
                    </div>
                  </div>
                </div>
              </div>
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
                      id="admin-file-upload"
                    />
                    <label 
                      htmlFor="admin-file-upload" 
                      style={{
                        background: 'linear-gradient(135deg, #228B22 0%, #1a6b1a 100%)',
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
                    background: '#e8f5e9', 
                    padding: '16px', 
                    borderRadius: '8px',
                    textAlign: 'left',
                    border: '1px solid #c8e6c9'
                  }}>
                    <h4 style={{ margin: '0 0 12px 0', color: '#2e7d32' }}>
                      ℹ️ Admin Print Workflow:
                    </h4>
                    <ol style={{ margin: 0, paddingLeft: '20px', color: '#555' }}>
                      <li>Upload your document (PDF, DOC, DOCX, TXT)</li>
                      <li>AI classifies as Official, Personal, or Confidential</li>
                      <li>System checks admin policy (100 pages/day, 100 copies, all categories allowed)</li>
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
                      ⚡ <strong>Admin Privilege:</strong> You have higher print limits and can print personal documents
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
                  // Optionally redirect or show a message
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
