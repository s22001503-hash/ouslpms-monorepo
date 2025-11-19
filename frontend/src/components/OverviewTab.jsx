import React from 'react'
import './OverviewTab.css'

export default function OverviewTab({ stats, role = 'admin' }) {
  const statCards = [
    {
      id: 'print-jobs',
      icon: '🖨️',
      label: 'Print Jobs Today',
      value: stats.todayPrintJobs || 0,
      change: '+12%',
      changeType: 'positive',
      bgGradient: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
      onClick: null
    },
    {
      id: 'pending-proposals',
      icon: role === 'vc' ? '⏳' : '⏳',
      label: role === 'vc' ? 'Pending Approvals' : 'Pending Proposals',
      value: stats.pendingProposals || 0,
      change: null,
      changeType: 'neutral',
      bgGradient: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
      onClick: null
    },
    {
      id: 'blocked-attempts',
      icon: '🚫',
      label: 'Blocked Attempts',
      value: stats.blockedAttempts || 0,
      change: '-5%',
      changeType: 'negative',
      bgGradient: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
      onClick: null
    },
    {
      id: 'active-users',
      icon: '👥',
      label: 'Active Users',
      value: stats.activeUsers || 0,
      change: '+3',
      changeType: 'positive',
      bgGradient: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
      onClick: null
    }
  ]

  return (
    <div className="overview-tab">
      <div className="overview-header">
        <h2>Dashboard Overview</h2>
        <p>Real-time system metrics and activity summary</p>
      </div>

      {/* Stat Cards Grid */}
      <div className="overview-stats-grid">
        {statCards.map(card => (
          <div
            key={card.id}
            className={`overview-stat-card ${card.onClick ? 'clickable' : ''}`}
            onClick={card.onClick}
            style={{ background: card.bgGradient }}
          >
            <div className="stat-card-icon">{card.icon}</div>
            <div className="stat-card-content">
              <div className="stat-card-value">{card.value}</div>
              <div className="stat-card-label">{card.label}</div>
              {card.change && (
                <div className={`stat-card-change ${card.changeType}`}>
                  {card.change}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Block Reasons Distribution */}
      <div style={{ marginTop: '32px' }}>
        <div style={{
          background: 'white',
          borderRadius: '12px',
          padding: '24px',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
        }}>
          <h3 style={{ margin: '0 0 20px 0', fontSize: '18px', fontWeight: 600, color: '#2d3748' }}>
            🚫 Block Reasons Distribution
          </h3>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '16px' }}>
            {/* Personal Documents */}
            <div style={{
              padding: '16px',
              border: '1px solid #fee2e2',
              borderRadius: '8px',
              background: 'linear-gradient(135deg, #fef2f2 0%, #fff 100%)'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <span style={{ fontSize: '14px', color: '#991b1b', fontWeight: 600 }}>Personal Documents</span>
                <span style={{ fontSize: '24px', fontWeight: 700, color: '#dc2626' }}>45</span>
              </div>
              <div style={{ width: '100%', height: '8px', background: '#fee2e2', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{ width: '60%', height: '100%', background: '#ef4444' }}></div>
              </div>
              <div style={{ marginTop: '4px', fontSize: '12px', color: '#991b1b' }}>60% of blocks</div>
            </div>

            {/* Daily Limit Exceeded */}
            <div style={{
              padding: '16px',
              border: '1px solid #fed7aa',
              borderRadius: '8px',
              background: 'linear-gradient(135deg, #fffbeb 0%, #fff 100%)'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <span style={{ fontSize: '14px', color: '#92400e', fontWeight: 600 }}>Daily Limit Exceeded</span>
                <span style={{ fontSize: '24px', fontWeight: 700, color: '#f59e0b' }}>20</span>
              </div>
              <div style={{ width: '100%', height: '8px', background: '#fed7aa', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{ width: '27%', height: '100%', background: '#f59e0b' }}></div>
              </div>
              <div style={{ marginTop: '4px', fontSize: '12px', color: '#92400e' }}>27% of blocks</div>
            </div>

            {/* Copy Limit Exceeded */}
            <div style={{
              padding: '16px',
              border: '1px solid #dbeafe',
              borderRadius: '8px',
              background: 'linear-gradient(135deg, #eff6ff 0%, #fff 100%)'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <span style={{ fontSize: '14px', color: '#1e40af', fontWeight: 600 }}>Copy Limit Exceeded</span>
                <span style={{ fontSize: '24px', fontWeight: 700, color: '#3b82f6' }}>10</span>
              </div>
              <div style={{ width: '100%', height: '8px', background: '#dbeafe', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{ width: '13%', height: '100%', background: '#3b82f6' }}></div>
              </div>
              <div style={{ marginTop: '4px', fontSize: '12px', color: '#1e40af' }}>13% of blocks</div>
            </div>
          </div>

          {/* Total Summary */}
          <div style={{
            marginTop: '20px',
            padding: '16px',
            background: 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)',
            borderRadius: '8px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            border: '1px solid #bbf7d0'
          }}>
            <div>
              <div style={{ fontSize: '14px', color: '#166534', marginBottom: '4px' }}>Total Blocked Attempts Today</div>
              <div style={{ fontSize: '12px', color: '#16a34a' }}>System is effectively preventing unauthorized prints</div>
            </div>
            <div style={{ fontSize: '32px', fontWeight: 700, color: '#16a34a' }}>75</div>
          </div>
        </div>
      </div>

    </div>
  )
}
