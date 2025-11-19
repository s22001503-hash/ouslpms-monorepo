/**
 * Agent API Client Service
 * =========================
 * 
 * TypeScript/JavaScript service for calling the SQLite REST API.
 * Provides methods to query the agent's local classification history database.
 * 
 * Base URL: http://localhost:8001
 * Authentication: X-API-Key header
 * 
 * Author: OUSL Print Management System
 * Date: October 29, 2025
 */

// ==================== CONFIGURATION ====================

const AGENT_API_URL = 'http://localhost:8001';
const API_KEY = 'ousl-sqlite-api-key-2025';

// ==================== API CLIENT CLASS ====================

class AgentApiClient {
  /**
   * Health check endpoint
   * No authentication required
   */
  async healthCheck() {
    const response = await fetch(`${AGENT_API_URL}/`);
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Get classification history with optional filters
   * 
   * @param {Object} options - Query options
   * @param {string} options.userId - Filter by user ID
   * @param {string} options.classification - Filter by classification
   * @param {string} options.action - Filter by action
   * @param {number} options.limit - Max records to return
   * @param {number} options.offset - Skip records (pagination)
   * @returns {Promise<Array>} Array of classification records
   */
  async getClassificationHistory(options = {}) {
    const params = new URLSearchParams();
    
    if (options.userId) params.append('user_id', options.userId);
    if (options.classification) params.append('classification', options.classification);
    if (options.action) params.append('action', options.action);
    if (options.limit) params.append('limit', options.limit.toString());
    if (options.offset) params.append('offset', options.offset.toString());

    return this.request('/api/classification-history', params);
  }

  /**
   * Get daily statistics for a user
   * 
   * @param {string} userId - User ID
   * @param {string} date - Date in YYYY-MM-DD format
   * @returns {Promise<Object>} Daily statistics
   */
  async getDailyStats(userId, date) {
    const params = new URLSearchParams({
      user_id: userId,
      date: date
    });

    return this.request('/api/daily-stats', params);
  }

  /**
   * Search classification history
   * 
   * @param {string} query - Search query
   * @param {string} field - Field to search (file_name, classification, user_id, action)
   * @param {number} limit - Max results
   * @returns {Promise<Object>} Search results
   */
  async search(query, field, limit = 100) {
    const params = new URLSearchParams({
      query: query,
      field: field,
      limit: limit.toString()
    });

    return this.request('/api/search', params);
  }

  /**
   * Get summary statistics
   * 
   * @returns {Promise<Object>} Overall statistics
   */
  async getSummaryStats() {
    return this.request('/api/stats/summary');
  }

  /**
   * Get list of users with statistics
   * 
   * @param {number} limit - Max users to return
   * @returns {Promise<Array>} Array of user info
   */
  async getUsers(limit = 100) {
    const params = new URLSearchParams({
      limit: limit.toString()
    });

    return this.request('/api/users', params);
  }

  // ==================== PRIVATE METHODS ====================

  /**
   * Get headers with API key
   * @private
   */
  getHeaders() {
    return {
      'X-API-Key': API_KEY,
      'Content-Type': 'application/json'
    };
  }

  /**
   * Make HTTP request to API
   * @private
   * 
   * @param {string} endpoint - API endpoint
   * @param {URLSearchParams} params - Query parameters
   * @returns {Promise<any>} Response data
   */
  async request(endpoint, params = null) {
    try {
      let url = `${AGENT_API_URL}${endpoint}`;
      if (params) {
        url += `?${params.toString()}`;
      }

      const response = await fetch(url, {
        method: 'GET',
        headers: this.getHeaders()
      });

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('Authentication failed. Invalid API key.');
        }
        throw new Error(`API request failed: ${response.statusText}`);
      }

      return response.json();
    } catch (error) {
      console.error('Agent API request failed:', error);
      throw error;
    }
  }
}

// ==================== SINGLETON EXPORT ====================

const agentApiClient = new AgentApiClient();

export default agentApiClient;
export { agentApiClient };
