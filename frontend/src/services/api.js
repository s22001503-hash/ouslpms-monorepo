// API service with automatic token refresh
import { getAuth } from 'firebase/auth'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

/**
 * Get a fresh Firebase Auth token (auto-refreshes if needed)
 */
async function getFreshToken() {
  const auth = getAuth()
  if (!auth.currentUser) {
    throw new Error('Not authenticated')
  }
  // Force refresh if token is close to expiring
  return await auth.currentUser.getIdToken(true)
}

/**
 * Verify Firebase ID token with backend
 */
export async function verifyToken(idToken) {
  const res = await fetch(`${API_BASE}/auth/verify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ idToken }),
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`Failed to verify token: ${res.status} ${text}`)
  }
  return res.json()
}

/**
 * Create a new user (admin only)
 */
export async function createUser(userData) {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/auth/create-user`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(userData),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to create user' }))
      throw new Error(error.detail || `Failed to create user: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    // Handle network errors specifically
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Delete a user by EPF (admin only)
 */
export async function deleteUser(epf) {
  try {
    console.log('Deleting user with EPF:', epf)
    console.log('API_BASE:', API_BASE)
    const token = await getFreshToken()
    console.log('Token obtained, making request...')
    const res = await fetch(`${API_BASE}/auth/delete-user`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ epf }),
    })
    console.log('Response received:', res.status, res.statusText)
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to delete user' }))
      throw new Error(error.detail || `Failed to delete user: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    console.error('Delete user error:', error)
    // Don't override authentication or other specific errors
    if (error.message === 'Not authenticated') {
      throw error
    }
    // Handle network errors specifically - fetch() throws TypeError for network issues
    if (error.name === 'TypeError' || error.message.toLowerCase().includes('failed to fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Change password for the authenticated user
 */
export async function changePassword(currentPassword, newPassword) {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/auth/change-password`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ currentPassword, newPassword }),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to change password' }))
      throw new Error(error.detail || `Failed to change password: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    // Handle network errors specifically
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Fetch admin overview statistics
 */
export async function fetchOverviewStats() {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/admin/overview`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to fetch overview stats' }))
      throw new Error(error.detail || `Failed to fetch overview stats: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Fetch current system settings
 */
export async function fetchSystemSettings() {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/system-settings`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to fetch system settings' }))
      throw new Error(error.detail || `Failed to fetch system settings: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Fetch settings proposal history for an admin
 */
export async function fetchSettingsRequests(adminId) {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/settings-requests?adminId=${adminId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to fetch settings requests' }))
      throw new Error(error.detail || `Failed to fetch settings requests: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Propose new system settings (admin only)
 */
export async function proposeSettings(proposal) {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/admin/propose-settings`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(proposal),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to propose settings' }))
      throw new Error(error.detail || `Failed to propose settings: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

// ==================== Dean-specific API calls ====================

/**
 * Fetch Dean overview statistics
 */
export async function fetchDeanOverview() {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/dean/overview`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to fetch dean overview' }))
      throw new Error(error.detail || `Failed to fetch dean overview: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Fetch settings proposals (pending by default)
 */
export async function fetchSettingsProposals(status = 'pending') {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/dean/settings-requests?status=${status}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to fetch proposals' }))
      throw new Error(error.detail || `Failed to fetch proposals: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Approve a settings proposal
 */
export async function approveSettingsProposal(proposalId, deanId, deanName, notes = '') {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/dean/settings/approve`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ proposalId, deanId, deanName, notes }),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to approve proposal' }))
      throw new Error(error.detail || `Failed to approve proposal: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Reject a settings proposal
 */
export async function rejectSettingsProposal(proposalId, deanId, deanName, reason = '') {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/dean/settings/reject`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ proposalId, deanId, deanName, reason }),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to reject proposal' }))
      throw new Error(error.detail || `Failed to reject proposal: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Fetch Dean notifications
 */
export async function fetchDeanNotifications() {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/dean/notifications`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to fetch notifications' }))
      throw new Error(error.detail || `Failed to fetch notifications: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Fetch Dean reports
 */
export async function fetchDeanReports() {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/dean/reports`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to fetch reports' }))
      throw new Error(error.detail || `Failed to fetch reports: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

// ==================== OLD Policy Management API calls - REMOVED (duplicates below) ====================

// ==================== Approval Requests API calls ====================

/**
 * Get user approval requests for VC review
 */
export async function getApprovalRequests(filter = 'all') {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/vc/approval-requests?filter=${filter}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to fetch approval requests' }))
      throw new Error(error.detail || `Failed to fetch approval requests: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Approve user print request (VC only)
 */
export async function approveUserRequest(requestId, vcId, notes = '') {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/vc/approval-requests/approve`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ requestId, vcId, notes }),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to approve request' }))
      throw new Error(error.detail || `Failed to approve request: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Reject user print request (VC only)
 */
export async function rejectUserRequest(requestId, vcId, reason) {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/vc/approval-requests/reject`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ requestId, vcId, reason }),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to reject request' }))
      throw new Error(error.detail || `Failed to reject request: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

// ==================== System Analytics API calls ====================

/**
 * Get system metrics and analytics
 */
export async function getSystemMetrics() {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/admin/system-metrics`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to fetch system metrics' }))
      throw new Error(error.detail || `Failed to fetch system metrics: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Export system report
 */
export async function exportReport(reportType, filters = {}) {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/admin/export-report`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ reportType, filters }),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to export report' }))
      throw new Error(error.detail || `Failed to export report: ${res.status}`)
    }
    return res.blob() // Return as blob for file download
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

// ==================== Policy Proposal API calls ====================

/**
 * Get user by EPF number
 */
export async function getUserByEPF(epf) {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/admin/user-by-epf/${epf}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'User not found' }))
      throw new Error(error.detail || `User not found: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Get current global policies
 */
export async function getCurrentPolicies() {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/admin/current-policies`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to fetch current policies' }))
      throw new Error(error.detail || `Failed to fetch current policies: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Propose a policy change (global or special user)
 * @param {Object} proposal - Proposal data
 * @param {string} proposal.type - 'global' or 'special_user'
 * @param {Object} proposal.changes - For global: { maxAttemptsPerDay: {current, proposed}, ... }
 * @param {Object} proposal.proposedPolicy - For special user: { maxAttemptsPerDay, maxCopiesPerDoc }
 * @param {string} proposal.targetEPF - For special user: target user's EPF
 * @param {string} proposal.justification - Justification text
 * @param {string} proposal.adminId - Admin's EPF
 */
export async function proposePolicyChange(proposal) {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/admin/propose-policy`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(proposal),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to submit policy proposal' }))
      throw new Error(error.detail || `Failed to submit policy proposal: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Get policy proposals (optionally filter by type and status)
 * @param {string} type - Optional: 'global', 'special_user', or undefined for all
 * @param {string} status - Optional: 'pending', 'approved', 'rejected', or undefined for all
 */
export async function getPolicyProposals(type = null, status = null) {
  try {
    const token = await getFreshToken()
    const params = new URLSearchParams()
    if (type) params.append('type', type)
    if (status) params.append('status', status)
    
    const url = `${API_BASE}/admin/policy-proposals${params.toString() ? '?' + params.toString() : ''}`
    const res = await fetch(url, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to fetch policy proposals' }))
      throw new Error(error.detail || `Failed to fetch policy proposals: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Get all users with active special policies
 */
export async function getSpecialPolicyUsers() {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/admin/special-policy-users`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to fetch special policy users' }))
      throw new Error(error.detail || `Failed to fetch special policy users: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Remove special policy from a user
 * @param {string} epf - User's EPF number
 */
export async function removeSpecialPolicy(epf) {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/admin/remove-special-policy`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ epf }),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to remove special policy' }))
      throw new Error(error.detail || `Failed to remove special policy: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Request removal of special policy (creates proposal for VC approval)
 * @param {string} epf - User's EPF number
 * @param {string} adminId - Admin's EPF number
 * @param {string} justification - Reason for removal
 */
export async function requestRemovalProposal(epf, adminId, justification) {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/admin/request-removal-proposal`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ 
        targetEpf: epf,
        requestedBy: adminId,
        justification 
      }),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to submit removal request' }))
      throw new Error(error.detail || `Failed to submit removal request: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

// ==================== VC Policy Management API calls ====================

/**
 * Approve a policy proposal (VC only)
 * @param {string} proposalId - Proposal ID
 * @param {string} vcId - VC's EPF
 * @param {string} notes - Optional approval notes
 */
export async function approvePolicyProposal(proposalId, vcId, notes = '') {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/vc/policy-proposals/approve`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ proposalId, vcId, notes }),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to approve policy proposal' }))
      throw new Error(error.detail || `Failed to approve policy proposal: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Reject a policy proposal (VC only)
 * @param {string} proposalId - Proposal ID
 * @param {string} vcId - VC's EPF
 * @param {string} reason - Rejection reason
 */
export async function rejectPolicyProposal(proposalId, vcId, reason) {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/vc/policy-proposals/reject`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ proposalId, vcId, reason }),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to reject policy proposal' }))
      throw new Error(error.detail || `Failed to reject policy proposal: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}




