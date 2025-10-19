import React from 'react'
import './OverviewTab.css'

export default function OverviewTab({ stats, onNavigate, quickActions = [] }) {
  const statCards = [
    {
      id: 'print-jobs',
      icon: '🖨️',
      label: 'Print Jobs Today',
      value: stats.todayPrintJobs || 0,
      change: '+12%',
      changeType: 'positive',
      bgGradient: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
      onClick: null // No specific action
    },
    {
      id: 'pending-proposals',
      icon: '⏳',
      label: 'Pending Proposals',
      value: stats.pendingProposals || 0,
      change: null,
      changeType: 'neutral',
      bgGradient: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
      onClick: () => onNavigate('settingsProposal')
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

      {/* Quick Actions */}
      {quickActions.length > 0 && (
        <div className="overview-quick-actions">
          <div className="quick-action-card">
            <h3>Quick Actions</h3>
            <div className="action-buttons">
              {quickActions.map((action, index) => (
                <button 
                  key={index} 
                  className="action-btn" 
                  onClick={() => onNavigate(action.view)}
                >
                  <span className="action-icon">{action.icon}</span>
                  {action.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
