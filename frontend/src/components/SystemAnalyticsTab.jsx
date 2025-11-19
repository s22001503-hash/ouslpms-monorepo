import React, { useState, useEffect } from 'react'
import './SystemAnalyticsTab.css'

/**
 * SystemAnalyticsTab - Real-time system monitoring and analytics
 */
export default function SystemAnalyticsTab() {
  const [metrics, setMetrics] = useState({
    todayPrints: 0,
    paperSaved: 0,
    blockedAttempts: 0,
    activeUsers: 0,
    systemHealth: 'healthy'
  })
  const [blockReasons, setBlockReasons] = useState([])
  const [topUsers, setTopUsers] = useState([])
  const [recentActivity, setRecentActivity] = useState([])
  const [autoRefresh, setAutoRefresh] = useState(true)

  useEffect(() => {
    loadMetrics()
    
    if (autoRefresh) {
      const interval = setInterval(loadMetrics, 30000) // Refresh every 30 seconds
      return () => clearInterval(interval)
    }
  }, [autoRefresh])

  const loadMetrics = async () => {
    // TODO: Replace with actual API call
    const mockMetrics = {
      todayPrints: 247,
      paperSaved: 1235, // sheets
      blockedAttempts: 45,
      activeUsers: 156,
      systemHealth: 'healthy', // healthy, warning, error
      aiServiceStatus: 'online',
      printersOnline: 12,
      printersTotal: 15
    }

    const mockBlockReasons = [
      { reason: 'Personal Document', count: 25, percentage: 55.6 },
      { reason: 'Daily Limit', count: 15, percentage: 33.3 },
      { reason: 'Copy Limit', count: 5, percentage: 11.1 }
    ]

    const mockTopUsers = [
      { name: 'John Smith', epf: '50123', prints: 18, department: 'Engineering' },
      { name: 'Sarah Johnson', epf: '50124', prints: 15, department: 'Science' },
      { name: 'Michael Brown', epf: '50125', prints: 12, department: 'Arts' },
      { name: 'Emily Davis', epf: '50126', prints: 10, department: 'Business' },
      { name: 'David Wilson', epf: '50127', prints: 9, department: 'Engineering' }
    ]

    const mockActivity = [
      { id: 1, user: 'John Smith', action: 'Print Approved', doc: 'Assignment.pdf', time: '2 min ago', type: 'success' },
      { id: 2, user: 'Sarah Johnson', action: 'Personal Doc Blocked', doc: 'Personal_Letter.pdf', time: '5 min ago', type: 'blocked' },
      { id: 3, user: 'Michael Brown', action: 'VC Approval Requested', doc: 'Research.pdf', time: '8 min ago', type: 'pending' },
      { id: 4, user: 'Emily Davis', action: 'Print Approved', doc: 'Report.pdf', time: '12 min ago', type: 'success' },
      { id: 5, user: 'David Wilson', action: 'Daily Limit Reached', doc: 'Notes.pdf', time: '15 min ago', type: 'blocked' }
    ]

    setMetrics(mockMetrics)
    setBlockReasons(mockBlockReasons)
    setTopUsers(mockTopUsers)
    setRecentActivity(mockActivity)
  }

  const getHealthColor = (health) => {
    const colors = {
      healthy: '#10b981',
      warning: '#f59e0b',
      error: '#ef4444'
    }
    return colors[health] || colors.healthy
  }

  const getHealthIcon = (health) => {
    const icons = {
      healthy: '✅',
      warning: '⚠️',
      error: '❌'
    }
    return icons[health] || icons.healthy
  }

  return (
    <div className="system-analytics-tab">
      <div className="sat-header">
        <div>
          <h2>📊 System Analytics</h2>
          <p>Real-time monitoring and statistics</p>
        </div>
        <div className="sat-header-controls">
          <label className="sat-auto-refresh">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
            />
            <span>Auto-refresh (30s)</span>
          </label>
          <button className="sat-btn refresh" onClick={loadMetrics}>
            🔄 Refresh
          </button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="sat-metrics-grid">
        <div className="sat-metric-card sat-primary">
          <div className="sat-metric-icon">📄</div>
          <div className="sat-metric-content">
            <div className="sat-metric-value">{metrics.todayPrints}</div>
            <div className="sat-metric-label">Total Prints Today</div>
          </div>
        </div>

        <div className="sat-metric-card sat-success">
          <div className="sat-metric-icon">🌱</div>
          <div className="sat-metric-content">
            <div className="sat-metric-value">{metrics.paperSaved}</div>
            <div className="sat-metric-label">Paper Sheets Saved</div>
          </div>
        </div>

        <div className="sat-metric-card sat-warning">
          <div className="sat-metric-icon">🚫</div>
          <div className="sat-metric-content">
            <div className="sat-metric-value">{metrics.blockedAttempts}</div>
            <div className="sat-metric-label">Blocked Attempts</div>
          </div>
        </div>

        <div className="sat-metric-card sat-info">
          <div className="sat-metric-icon">👥</div>
          <div className="sat-metric-content">
            <div className="sat-metric-value">{metrics.activeUsers}</div>
            <div className="sat-metric-label">Active Users</div>
          </div>
        </div>
      </div>

      {/* System Health */}
      <div className="sat-section">
        <h3>🏥 System Health</h3>
        <div className="sat-health-grid">
          <div className="sat-health-card">
            <div className="sat-health-status" style={{ color: getHealthColor(metrics.systemHealth) }}>
              {getHealthIcon(metrics.systemHealth)} System Status
            </div>
            <div className="sat-health-value">{metrics.systemHealth.toUpperCase()}</div>
          </div>

          <div className="sat-health-card">
            <div className="sat-health-status">🤖 AI Classification Service</div>
            <div className="sat-health-value">
              <span className="sat-status-dot sat-online"></span>
              {metrics.aiServiceStatus?.toUpperCase()}
            </div>
          </div>

          <div className="sat-health-card">
            <div className="sat-health-status">🖨️ Printers</div>
            <div className="sat-health-value">
              {metrics.printersOnline}/{metrics.printersTotal} ONLINE
            </div>
          </div>
        </div>
      </div>

      {/* Block Reasons Chart */}
      <div className="sat-section">
        <h3>🚫 Block Reasons Distribution</h3>
        <div className="sat-block-reasons">
          {blockReasons.map((item, index) => (
            <div key={index} className="sat-block-item">
              <div className="sat-block-label">
                <span>{item.reason}</span>
                <span className="sat-block-count">{item.count}</span>
              </div>
              <div className="sat-block-bar">
                <div 
                  className="sat-block-fill" 
                  style={{ width: `${item.percentage}%` }}
                ></div>
              </div>
              <div className="sat-block-percentage">{item.percentage}%</div>
            </div>
          ))}
        </div>
      </div>

      <div className="sat-row">
        {/* Top Users */}
        <div className="sat-section sat-half">
          <h3>🏆 Top Users Today</h3>
          <div className="sat-top-users">
            {topUsers.map((user, index) => (
              <div key={index} className="sat-user-item">
                <div className="sat-user-rank">{index + 1}</div>
                <div className="sat-user-info">
                  <div className="sat-user-name">{user.name}</div>
                  <div className="sat-user-dept">{user.department} • EPF: {user.epf}</div>
                </div>
                <div className="sat-user-count">{user.prints} prints</div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="sat-section sat-half">
          <h3>⚡ Recent Activity</h3>
          <div className="sat-activity-list">
            {recentActivity.map(activity => (
              <div key={activity.id} className={`sat-activity-item sat-${activity.type}`}>
                <div className="sat-activity-user">{activity.user}</div>
                <div className="sat-activity-action">{activity.action}</div>
                <div className="sat-activity-doc">{activity.doc}</div>
                <div className="sat-activity-time">{activity.time}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Export Actions */}
      <div className="sat-section">
        <h3>📥 Export Reports</h3>
        <div className="sat-export-buttons">
          <button className="sat-btn primary">
            📊 Export Daily Report (CSV)
          </button>
          <button className="sat-btn primary">
            📈 Export Weekly Report (CSV)
          </button>
          <button className="sat-btn primary">
            📉 Export Department Analysis (CSV)
          </button>
        </div>
      </div>
    </div>
  )
}
