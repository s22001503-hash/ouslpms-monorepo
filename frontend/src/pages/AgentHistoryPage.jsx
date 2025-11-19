/**
 * Example Usage Page - Agent Print History
 * =========================================
 * 
 * Demonstrates how to use the AgentPrintHistory component.
 * 
 * This page shows the local print classification history
 * from the agent's SQLite database via REST API.
 * 
 * Author: OUSL Print Management System
 * Date: October 29, 2025
 */

import AgentPrintHistory from '../components/AgentPrintHistory';

const AgentHistoryPage = () => {
  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Agent Database Monitor</h1>
        <p>View local print classification history from agent's SQLite database</p>
      </div>

      <AgentPrintHistory />

      <div className="page-footer">
        <p className="info-text">
          <strong>Note:</strong> This data is fetched from the agent's local SQLite database via REST API (localhost:8001).
          Make sure the SQLite API server is running.
        </p>
        <div className="commands">
          <h4>Start SQLite API Server:</h4>
          <code>cd backend && python sqlite_api_server.py</code>
        </div>
      </div>
    </div>
  );
};

export default AgentHistoryPage;
