/**
 * Agent Print History Component
 * ==============================
 * 
 * Displays local print classification history from agent's SQLite database.
 * 
 * Features:
 * - View classification records
 * - Filter by user, classification, action
 * - Pagination
 * - Real-time statistics
 * - Search functionality
 * 
 * Author: OUSL Print Management System
 * Date: October 29, 2025
 */

import { useState, useEffect } from 'react';
import agentApiClient from '../services/agentApi';
import './AgentPrintHistory.css';

// ==================== COMPONENT ====================

const AgentPrintHistory = () => {
  // State
  const [history, setHistory] = useState([]);
  const [dailyStats, setDailyStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({});
  const [page, setPage] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  
  const RECORDS_PER_PAGE = 50;

  // ==================== DATA FETCHING ====================

  /**
   * Fetch classification history
   */
  const fetchHistory = async () => {
    try {
      setLoading(true);
      setError(null);

      const records = await agentApiClient.getClassificationHistory({
        userId: filters.userId,
        classification: filters.classification,
        action: filters.action,
        limit: RECORDS_PER_PAGE,
        offset: page * RECORDS_PER_PAGE,
      });

      setHistory(records);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch history');
      console.error('Error fetching history:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Fetch daily stats for current user
   */
  const fetchDailyStats = async (userId) => {
    try {
      const today = new Date().toISOString().split('T')[0];
      const stats = await agentApiClient.getDailyStats(userId, today);
      setDailyStats(stats);
    } catch (err) {
      console.error('Error fetching daily stats:', err);
    }
  };

  /**
   * Search history
   */
  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      fetchHistory();
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const results = await agentApiClient.search(searchQuery, 'file_name');
      setHistory(results.results);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed');
    } finally {
      setLoading(false);
    }
  };

  // ==================== EFFECTS ====================

  useEffect(() => {
    fetchHistory();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters, page]);

  useEffect(() => {
    if (filters.userId) {
      fetchDailyStats(filters.userId);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters.userId]);

  // ==================== HELPERS ====================

  const getActionBadge = (action) => {
    if (action === 'allow') {
      return <span className="badge badge-success">✅ Allowed</span>;
    }
    return <span className="badge badge-danger">❌ Blocked</span>;
  };

  const getClassificationBadge = (classification) => {
    const badges = {
      office: 'badge-primary',
      personal: 'badge-warning',
      confidential: 'badge-danger',
    };

    return (
      <span className={`badge ${badges[classification] || 'badge-secondary'}`}>
        {classification}
      </span>
    );
  };

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return 'N/A';
    return new Date(timestamp).toLocaleString();
  };

  // ==================== RENDER ====================

  return (
    <div className="agent-print-history">
      <div className="header">
        <h2>📊 Local Print History (Agent Database)</h2>
        <p className="text-muted">
          Classification records from agent's SQLite database
        </p>
      </div>

      {/* Statistics Card */}
      {dailyStats && (
        <div className="stats-card">
          <h4>Today's Statistics - User {dailyStats.user_id}</h4>
          <div className="stats-grid">
            <div className="stat">
              <span className="stat-label">Total Attempts</span>
              <span className="stat-value">{dailyStats.total_attempts}</span>
            </div>
            <div className="stat">
              <span className="stat-label">Allowed</span>
              <span className="stat-value text-success">{dailyStats.allowed}</span>
            </div>
            <div className="stat">
              <span className="stat-label">Blocked</span>
              <span className="stat-value text-danger">{dailyStats.blocked}</span>
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="filters">
        <div className="filter-group">
          <label>User ID</label>
          <input
            type="text"
            value={filters.userId || ''}
            onChange={(e) => setFilters({ ...filters, userId: e.target.value })}
            placeholder="e.g., 99999"
          />
        </div>

        <div className="filter-group">
          <label>Classification</label>
          <select
            value={filters.classification || ''}
            onChange={(e) => setFilters({ ...filters, classification: e.target.value })}
          >
            <option value="">All</option>
            <option value="office">Office</option>
            <option value="personal">Personal</option>
            <option value="confidential">Confidential</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Action</label>
          <select
            value={filters.action || ''}
            onChange={(e) => setFilters({ ...filters, action: e.target.value })}
          >
            <option value="">All</option>
            <option value="allow">Allowed</option>
            <option value="block">Blocked</option>
          </select>
        </div>

        <button onClick={() => setFilters({})}>Clear Filters</button>
      </div>

      {/* Search */}
      <div className="search-bar">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search by filename..."
          onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="alert alert-danger">
          <strong>Error:</strong> {error}
          <p className="text-muted">
            Make sure the SQLite API server is running on port 8001.
          </p>
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading history...</p>
        </div>
      )}

      {/* Records Table */}
      {!loading && history.length > 0 && (
        <div className="records-table">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Timestamp</th>
                <th>User</th>
                <th>File Name</th>
                <th>Classification</th>
                <th>Action</th>
                <th>Copies</th>
                <th>Reason</th>
              </tr>
            </thead>
            <tbody>
              {history.map((record) => (
                <tr key={record.id}>
                  <td>{record.id}</td>
                  <td>{formatTimestamp(record.timestamp)}</td>
                  <td>{record.user_id}</td>
                  <td title={record.file_name}>
                    {record.file_name && record.file_name.length > 30
                      ? `${record.file_name.substring(0, 30)}...`
                      : record.file_name}
                  </td>
                  <td>{getClassificationBadge(record.classification || 'unknown')}</td>
                  <td>{getActionBadge(record.action || 'unknown')}</td>
                  <td>{record.copies}</td>
                  <td title={record.reason}>
                    {record.reason && record.reason.length > 50
                      ? `${record.reason.substring(0, 50)}...`
                      : record.reason}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Empty State */}
      {!loading && history.length === 0 && !error && (
        <div className="empty-state">
          <p>📭 No records found</p>
          <p className="text-muted">
            Try adjusting your filters or search query
          </p>
        </div>
      )}

      {/* Pagination */}
      {!loading && history.length > 0 && (
        <div className="pagination">
          <button
            onClick={() => setPage(Math.max(0, page - 1))}
            disabled={page === 0}
          >
            Previous
          </button>
          <span>Page {page + 1}</span>
          <button
            onClick={() => setPage(page + 1)}
            disabled={history.length < RECORDS_PER_PAGE}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default AgentPrintHistory;
